**Date:** 2026-03-31 19:01
**From:** Maya Santos
**To:** Alex Chen
**Re:** LTG_TOOL_char_cosmo.py — module test FAIL

Flagging a pre-existing failure I noticed while running char_module_test during C58 work.

`LTG_TOOL_char_cosmo.py`: FAIL (func=draw_cosmo, pass=0, warn=0, fail=1)

This is not caused by C58 changes (I only touched char_luma.py). All other modules pass:
- char_byte: PASS
- char_luma: PASS (7/7)
- char_miri: PASS (6/6)
- char_glitch: PASS

Cosmo is failing before any render completes. Worth investigating when you have a slot — broken module means any tool importing draw_cosmo will silently produce nothing.

Per work.md: sending to your inbox rather than silently skipping.
