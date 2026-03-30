**Date:** 2026-03-30
**From:** Alex Chen
**Subject:** C49 — CRT glow asymmetry fix

Rin,

New rule codified in `docs/image-rules.md`: **CRT Glow Asymmetry Rule (C49)**.

Real CRT glow is brighter above and to the sides, dimmer below (cabinet/desk occlusion). All CRT glow generators need a **0.70 multiplier** on glow alpha/intensity for pixels below the screen's vertical midpoint.

**Your tasks this cycle:**

1. **Update all CRT glow generators** you own to apply the 0.70 below-midpoint multiplier. This includes any GL showcase, scanline, or CRT-emitting scene generators.
2. **UV_PURPLE hue center evaluation** (carried from C48): Reference glitch art clusters 280-290 degrees. Our current UV_PURPLE is centered at 270. Evaluate whether a shift to ~275 improves fidelity. If yes, update the constant and flag any downstream generators affected.
3. Regenerate affected assets after the glow fix.

Read the full rule in `docs/image-rules.md` under "CRT Glow Asymmetry Rule" for thresholds and exemptions.

Priority: CRT glow fix first, UV_PURPLE eval second.

— Alex
