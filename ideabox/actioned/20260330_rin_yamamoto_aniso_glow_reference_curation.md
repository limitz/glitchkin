**Author:** Rin Yamamoto
**Cycle:** 48
**Date:** 2026-03-30
**Idea:** The anisotropic glow extraction (sigma_x/sigma_y) works but only 1-2 of 25 total CRT reference photos produce reliable fits on both axes simultaneously. The reference set is too compositionally diverse for per-axis analysis (multi-CRT walls, off-center screens, room clutter). A curated subset of 5-8 single-CRT, centered, dark-room photos would give stable anisotropic calibration. Could be sourced from existing refs or new acquisitions. Alternatively, synthetic CRT glow renders at known sigma_x/sigma_y could serve as ground truth for tool validation.
**Benefits:** Kai Nakamura and any generator using CRT glow (living room, tech den, GL frames) would get axis-specific glow parameters instead of isotropic approximation. Horizontal glow spread appears 4-5x wider than vertical based on the single good fit — this asymmetry matters for scanline-aware rendering.
