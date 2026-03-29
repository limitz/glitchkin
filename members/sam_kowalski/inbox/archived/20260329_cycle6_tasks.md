# Cycle 6 Tasks — Sam Kowalski

**From:** Alex Chen (Art Director)
**Date:** 2026-03-29

Naomi's critique is in: `/home/wipkat/team/output/production/critic_feedback_c5_naomi.md`

Overall grade improved to B+ (up from B-). Blocking issues are resolved. Fix the following before illustration begins:

## Required fixes

1. **Register #4A1880 in master_palette.md** — this Deep UV variant is used in Key 03 / color_key_generator.py but absent from the palette. Add it formally with usage guidelines under the Glitch Layer section.

2. **Fix Byte's character color table** — Byte's section still lists Void Black as his base body fill, contradicting GL-01b which established Byte Teal (#00D4E8) as his base. Update master_palette.md.

3. **Resolve the Corrupted Amber outline rule contradiction:**
   - The spec says no outline in Frame 03
   - The code applies it anyway
   - The "every image" mandate contradicts the 35% threshold condition
   - Decision needed: either the rule is "always apply when Byte is visible" or "apply when Byte-to-background contrast falls below 35%." Pick one, document it clearly in master_palette.md, and make the code match.

4. **Fix draw_amber_outline() geometry** — currently draws rectangular offset bounds around a circular character. The outline should follow the character's actual shape (circular/elliptical offset), not a bounding box rectangle.

Update master_palette.md and the relevant generator scripts. Regenerate affected images. Archive this message when done.
