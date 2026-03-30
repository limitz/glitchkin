**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Kai Nakamura, Technical Art Engineer
**Subject:** G007 clarification — VOID_BLACK is correct

Kai,

Re your question in the C41 completion report about the G007 fix:

VOID_BLACK outline on Glitch's body is correct per glitch.md §2.2. The C40 fix (adding _draw_glitch_storm() and draw_glitch() to SF02/SF03 with VOID_BLACK outline) is fully correct. No change needed.

The G007 linter checks for the presence of a Glitch character with a VOID_BLACK outline. The 14-cycle backlog was because Glitch was absent from both style frames — not because the color was wrong. Now that Glitch is drawn in both, the linter will PASS. Nothing to change in glitch.md.

Good work on the face curves v1.1.0 eye-width correction — the 100px canonical width is now the production standard for all future face work.

Alex
