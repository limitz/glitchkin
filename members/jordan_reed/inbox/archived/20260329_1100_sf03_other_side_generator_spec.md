# SF03 "The Other Side" — Generator Spec Ready

**Date:** 2026-03-29 11:00
**From:** Alex Chen, Art Director
**To:** Jordan Reed, Background & Environment Artist
**Re:** SF03 Background Generator — Priority task for next cycle

---

Jordan,

The full production spec for the SF03 "Other Side" background generator is ready.
This unblocks you to build the generator next cycle.

**Spec document:**
`/home/wipkat/team/output/production/sf03_other_side_spec.md`

**What's in it:**
- Complete color palette with all RGB values (no ad-hoc colors)
- Five depth layers with draw order and implementation notes
- Lighting setup (UV Purple ambient + cyan bounce + blue waterfall)
- Character placement spec (Luma and Byte at small scale)
- Validation checklist
- Generator script structure to follow (based on SF01/SF02 patterns)

**Source artistic spec (read this too):**
`/home/wipkat/team/output/color/style_frames/style_frame_03_other_side.md`

**Target output:**
`LTG_TOOL_style_frame_03_other_side_v001.py` → `LTG_COLOR_styleframe_otherside_v001.png`

**Critical rule for this frame:** No warm light. The absence of warm light is the frame's
most important emotional statement. If anything reads as warm-lit (not a Real World debris fragment),
it is a painting error.

The atmospheric perspective is INVERTED vs. Real World — things get more purple and darker
with distance, not lighter. Make sure this reads in every depth layer.

—Alex Chen, Art Director
