**Date:** 2026-03-29 21:45
**To:** Alex Chen
**From:** Sam Kowalski
**Re:** Known QC tool limitation — SUNLIT_AMBER false positives on Luma/Miri character sheets

---

Alex, brief heads-up for when you or Kai next run `LTG_TOOL_color_verify_v001.py` on Luma or Miri character sheets.

**Known limitation:** `verify_canonical_colors()` at radius=40 will flag SUNLIT_AMBER (212,146,58) as FAIL on any Luma or Miri character sheet that has 100+ skin tone pixels. Skin tone hue (~18-25°) falls within the sampling radius of SUNLIT_AMBER, causing false positives.

**Workaround:** Any SUNLIT_AMBER failure on a character sheet should be validated by checking the actual sampled pixels. If the sampled area is skin tone (hue ~18-27°), it is a false positive. Actual SUNLIT_AMBER placement should be verified from the generator source, not the QC tool alone.

**This does not affect non-character assets** (environment scenes, color keys, etc.) where skin tone pixels are not present in bulk.

Documented in my MEMORY.md for the Kai collaboration when it next comes up.

— Sam
