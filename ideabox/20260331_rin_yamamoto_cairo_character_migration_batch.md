**Date:** 2026-03-31
**From:** Rin Yamamoto
**Subject:** Batch-migrate remaining character generators to pycairo

With Byte and Glitch now fully running on pycairo, the remaining PIL-based character
generators (Luma, Cosmo, Miri, Grandma Miri) should be migrated in a single batch cycle.

Benefits observed from C52 rebuild:
- AA ratio improvement (native sub-pixel AA vs PIL's binary edges)
- Wobble outlines give organic hand-drawn quality without post-processing
- Cairo clipping makes shadow/highlight composition much cleaner than PIL polygon hacks
- Bezier curves for scar lines, crack forks, and confetti trails
- Render time stays <10ms per character even with full AA

Proposal: one cycle dedicated to migrating the 4 remaining character expression sheets
+ turnarounds. Prioritize Luma (most complex, most screen time) first, then Cosmo,
then Miri and Grandma Miri together (simpler geometry).

Migration checklist per character:
1. Replace PIL draw calls with cairo equivalents
2. Add wobble outlines (amplitude calibrated per character)
3. Add bezier confetti/detail trails where applicable
4. Verify AA ratio improvement via edge analysis
5. Run face test gate
6. Overwrite existing PNGs in place
