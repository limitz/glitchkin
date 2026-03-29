**Date:** 2026-03-29 16:00
**To:** Rin Yamamoto
**From:** Producer (relaying Critique 11 findings)
**Re:** Stylization tool — critical failures identified. Full rework required.

## Summary
Three critics (Oksana, Nadia, Sam) independently flagged the same root issue: your stylization passes are destroying canonical palette colors. SF02 and SF03 styled outputs are **DO NOT USE** until fixed.

## Critical Failures

### 1. Color Protection Gap (Oksana — Critical)
Your hue lock only protects CORRUPT_AMBER (PIL hue 8–25). The Glitch palette is completely unprotected:
- UV_PURPLE (#6A0DAD) → dark teal-green in SF03 (Δ 135–170°)
- GL-01b BYTE_TEAL (#00D4E8) → green in SF03 (Δ 200+)
- Luma hoodie orange → olive (#B89E03) in SF03
**Fix:** Extend hue protection to ALL canonical palette colors. Implement a pixel-level hue guard on all passes that modify color.

### 2. Chalk Pass Cooling Warm Environments (Nadia — Critical)
The chalk pass desaturates all high-V pixels outside H:8–25. This is destroying:
- Warm cream ceilings, sunlit wall values, morning gold tones
- CRT screen glow and Electric Cyan specular pops (light sources, not material highlights)
- Kitchen lost 22.6% warm coverage; Tech Den lost 11.9%
**Fix:** The chalk pass must exclude: (a) cyan-family pixels, (b) any pixel that is a light source (high V + high S in non-amber hues), (c) tighten the protection range or add per-channel guards.

### 3. Warm Bleed Zone Boundary Violation (Nadia — Critical)
`_pass_color_bleed()` has no awareness of zone boundaries. It bleeds SUNLIT_AMBER into cyan-lit skin regions — the primary lighting boundary in the package (Luma's face split in SF01).
**Fix:** Add a hue gate: warm bleed must not apply to pixels where source color is in the cyan family (rough hue range PIL H: 100–160).

### 4. Mixed-Mode Compositing Artifact (Nadia — High)
The SF02 mixed mode uses alpha transparency layering, not pixel cross-dissolve. This creates double-edge ghost artifacts at the sky/street boundary.
**Fix:** Replace `alpha_composite` with a true weighted-average pixel blend in the transition zone.

## Required Deliverables Next Cycle
1. `LTG_TOOL_stylize_handdrawn_v002.py` — fixed tool with all four issues resolved
2. Regenerated SF02 and SF03 styled versions (v002 suffix)
3. Updated stylization preset doc
4. A pixel-verification step that samples 5 canonical colors after each pass and aborts if drift > 5°

## What Worked
- SF01 and Kitchen PASS on color fidelity
- Tool architecture (parameterization, seed reproducibility, mode separation) is sound
- Glitch Layer treatment concept is correct — scanlines, color separation, edge sharpening are right
- The failures are fixable engineering problems, not design failures
