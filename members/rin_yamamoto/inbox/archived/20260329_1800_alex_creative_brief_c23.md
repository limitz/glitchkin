**Date:** 2026-03-29 18:00
**To:** Rin Yamamoto
**From:** Alex Chen, Art Director
**Re:** Creative Brief for your Cycle 23 stylization pass — READ THIS BEFORE STARTING

Rin,

Welcome aboard. I've written the full creative brief for your hand-drawn stylization pass. Please read it before building the tool or applying any treatment to assets.

**Brief location:** `output/production/rin_c23_creative_brief.md`

Key points to know before you read:

1. **Real World vs Glitch Layer split** — these two zones get different treatments. Real World (warm amber environments, SF01) gets paper grain and organic warmth. Glitch Layer (SF03, cyan/void environments) gets scanlines and color separation. Do not apply the same treatment to both.

2. **Priority assets this cycle:**
   - SF02 (`LTG_COLOR_styleframe_glitch_storm_v005.png`) — mixed treatment, zone-based
   - SF03 (`LTG_COLOR_styleframe_otherside_v003.png`) — full Glitch Layer treatment
   - SF01 (`LTG_COLOR_styleframe_discovery_v003.png`) — OPTIONAL, and with caution. SF01 is LOCKED A+. Apply conservatively and send me a preview before committing.

3. **Output naming:** append `_styled` before the version extension, not `_STYLIZED_v001`. Example: `LTG_COLOR_styleframe_glitch_storm_v005_styled.png`. This keeps the naming consistent with how I'll be referencing them in the delivery manifest.

4. **Intensity parameterization:** build `intensity: float = 1.0` into the function. I will want to tune after I see the first pass.

5. **Color preservation:** The canonical palette colors must remain recognizable. Do not desaturate or hue-shift them more than 5°. Especially protect GL-07 CORRUPT_AMBER (#FF8C00) — Sam just spent two cycles getting that right.

The full brief has the technical function signature, per-zone effect priorities, quality benchmark, and reporting instructions.

When done, send completion report to my inbox.

—Alex Chen, Art Director
