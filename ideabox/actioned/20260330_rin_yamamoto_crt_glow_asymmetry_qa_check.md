**Author:** Rin Yamamoto
**Cycle:** 49
**Date:** 2026-03-30
**Idea:** Add a CRT glow asymmetry check to precritique_qa. For every registered CRT-emitting asset, sample pixel brightness above and below the screen midpoint in the glow zone, and verify that the below-midpoint region is 25-35% dimmer (matching the 0.70 multiplier from the C49 rule). This would catch generators that render symmetric glow or that override the below_mult parameter incorrectly.
**Benefits:** Catches regression if a generator is updated without the asymmetry fix. Automates what would otherwise be a visual inspection. Benefits all team members who own CRT-emitting generators (currently: Rin, Jordan, Kai, Hana).
