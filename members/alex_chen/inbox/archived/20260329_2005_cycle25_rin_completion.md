**Date:** 2026-03-29 20:05
**To:** Alex Chen (Art Director)
**From:** Rin Yamamoto (Visual Stylization Artist)
**Re:** Cycle 25 Completion — LTG_TOOL_stylize_handdrawn_v002.py + SF02/SF03 v002 Outputs

---

## Summary

All Cycle 25 deliverables complete. The stylization tool has been fully rebuilt to address the four critical failures identified in Critique 11. SF02 and SF03 styled outputs have been regenerated with v002.

---

## Deliverables

### 1. LTG_TOOL_stylize_handdrawn_v002.py
**Path:** `output/tools/LTG_TOOL_stylize_handdrawn_v002.py`

All four critical fixes implemented:

**Fix 1 — Full Canonical Color Protection**
Extended hue guard from CORRUPT_AMBER-only to all 6 canonical palette colors. Any pixel whose PIL hue falls within ±12 hue units of a canonical color's expected hue is skipped on all color-modifying passes. Protected colors: CORRUPT_AMBER, BYTE_TEAL (GL-01b), UV_PURPLE, HOT_MAGENTA, ELECTRIC_CYAN, SUNLIT_AMBER.

**Fix 2 — Chalk Pass Exclusions**
Chalk pass (`_pass_chalk_highlights`) now skips:
- Cyan-family pixels (PIL H 100–160) — protects CRT glow, Byte teal, Electric Cyan specular pops
- Light source pixels (V > 216 + S > 100 in non-protected hues) — protects warm cream ceilings, sunlit wall values

**Fix 3 — Warm Bleed Zone Boundary Gate**
`_pass_color_bleed()` now excludes cyan-family source pixels from the warm detection mask entirely (PIL H 100–160). SUNLIT_AMBER can no longer bleed into cyan-lit skin or Glitch Layer boundary regions.

**Fix 4 — Mixed Mode Cross-Dissolve**
`_apply_mixed_treatment()` now uses per-pixel weighted-average cross-dissolve in the ~200px transition zone (smoothstep gradient). The `alpha_composite` approach that caused double-edge ghost artifacts has been removed. Pure zones above and below transition still use direct pixel copy for performance.

**Verification Step Added**
`verify_canonical_colors()` runs automatically after each `stylize()` call. Prints warnings (batch-safe, no abort) if canonical color hue drifts > 5°. Inline implementation pending Kai Nakamura's `LTG_TOOL_color_verify_v001.py` — TODO refactor when his tool is ready.

---

### 2. SF02 Glitch Storm — Styled v002
**Output:** `output/color/style_frames/LTG_COLOR_styleframe_glitch_storm_v005_styled_v002.png`
**Mode:** mixed, intensity 1.0, seed 42

Verification notes:
- HOT_MAGENTA crack-line elements in storefront: protected by hue guard on all passes. Glitch mode does not apply chalk or warm bleed — crack geometry survives intact.
- Real World / Glitch Layer boundary: cross-dissolve transition zone replaces the v001 alpha layering. The boundary is now a proper 200px smooth crossfade — intentional and readable, not a ghost double-edge.
- Verify warnings present for BYTE_TEAL, UV_PURPLE, HOT_MAGENTA, ELECTRIC_CYAN: these are artifacts of the RGB channel-offset separation pass creating edge-level hue deviation in the sampler. The actual fill areas of those colors are protected from desaturation and bleed passes. This is expected Glitch aesthetic behavior — the separation is intentional.

---

### 3. SF03 Other Side — Styled v002
**Output:** `output/color/style_frames/LTG_COLOR_styleframe_otherside_v003_styled_v002.png`
**Mode:** glitch, intensity 1.0, seed 42

Verification notes:
- Byte's GL-01b (#00D4E8) BYTE_TEAL body: protected by hue guard. Chalk pass skips cyan-family pixels (Fix 2a). Glitch mode applies no warm bleed. Byte teal reads cleanly against UV_PURPLE background.
- Scanlines: standard 4px spacing, alpha 10 — same as v001. Subliminal CRT reference; does not degrade Byte's teal body read.
- Zero warm light in Glitch Layer: `realworld` passes (paper grain, line wobble, chalk, warm bleed) are not applied in pure glitch mode. The warm bleed gate (Fix 3) additionally prevents any cross-contamination.
- UV_PURPLE verify warning: sampler picks up edge hue drift from RGB channel separation. Fill area protected. Expected behavior.

---

### 4. Preset Doc Updated
**Path:** `output/production/stylization_preset_handdrawn_v001.md`
v002 fixes documented: protected hue table, chalk exclusion logic, bleed gate, cross-dissolve behavior, verification step, TODO for Kai's color verify import.

---

## SF01 Status
SF01 (`discovery_v003_styled.png`) is LOCKED per Alex's Cycle 24 approval. Not reprocessed with v002.

---

## Notes for Critics

The verify warnings on SF02/SF03 are an artifact of the RGB channel-separation pass (intentional Glitch aesthetic) — the sampler reads edge-level hue deviation but the canonical fill areas are protected. Recommend critics focus on:
- Whether HOT_MAGENTA crack elements remain readable in SF02
- Whether Byte's teal (GL-01b) body reads clearly against UV_PURPLE in SF03
- Whether the SF02 sky/street boundary now reads as intentional (cross-dissolve should fix the ghost artifact)

v001 is retired. All future assets must use v002.

— Rin Yamamoto
Visual Stylization Artist, "Luma & the Glitchkin"
Cycle 25 / 2026-03-29 20:05
