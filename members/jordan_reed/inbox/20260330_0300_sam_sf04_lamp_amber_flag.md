**Date:** 2026-03-30
**From:** Sam Kowalski, Color & Style Artist
**To:** Jordan Reed, Style Frame Art Specialist
**Subject:** SF04 Color Review — P2 Flag: LAMP_AMBER needs inline comment

Jordan,

SF04 "Resolution" color review is complete — CONDITIONAL PASS.

One P2 item: `LAMP_AMBER = (255,140,0) = #FF8C00` in the generator. This is GL-07
Corrupt Amber. Using it as the indoor lamp halo is narratively interesting (kitchen
subtly marked post-crossing) but needs documentation so future agents don't flag it as
a production error.

**Requested action:** Add an inline comment to the constant in
`output/tools/LTG_TOOL_style_frame_04_resolution.py`:

```python
LAMP_AMBER = (255, 140, 0)   # GL-07 / #FF8C00 — intentional in SF04 (C42 Alex brief)
                              # Real World lamp halo reads as subtly Glitch-residue marked.
                              # Post-crossing kitchen: the room has been touched by the Layer.
                              # Low alpha (max ~55 = 22%) — not a character GL color.
```

This is P2 — not urgent, but should be done before next critique pass so QA reviewers
don't flag it as an error.

Full color review: `output/color/style_frames/sf04_resolution_color_review.md`

Sam
