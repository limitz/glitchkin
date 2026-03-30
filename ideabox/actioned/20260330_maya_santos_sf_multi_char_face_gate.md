**Author:** Maya Santos
**Cycle:** 48
**Date:** 2026-03-30
**Idea:** Add a multi-character style frame face gate mode to LTG_TOOL_character_face_test.py. Currently the face gate tests one character at a time at a fixed head_r. For style frames with two or more characters (like SF06), the tool should accept an image path, detect each character's head region at actual in-frame scale, and run the face gate per character. This would replace manual visual inspection for multi-char SFs.
**Benefits:** Jordan Reed, Lee Tanaka, Maya Santos, Rin Yamamoto — anyone producing style frames with multiple characters. Eliminates the gap where SF face quality is only visually inspected while expression sheets get automated checks.
