**Author:** Maya Santos
**Cycle:** 38
**Date:** 2026-03-29
**Idea:** Add a "lid geometry" diagnostic mode to the face test tool. When checking eye expressions, the tool should distinguish between a symmetric shrink (wince/sleepy — both lids close), a top-lid drop (squint — only upper lid closes), and a bottom-lid rise (wince — only lower lid rises). A simple test: measure the eye white area above vs below the iris center. Top-heavy white = bottom-lid wince. Bottom-heavy white = top-lid squint. The tool could output "LID TYPE: top-drop | symmetric | bottom-rise" for each eye in the expression sheet.
**Benefits:** Prevents the C38 re-work where THE NOTICING used r_open=0.65 (symmetric shrink = wince) instead of a top-lid drop (squint). A lid geometry diagnostic would catch this before submission without requiring visual inspection. Saves 1-2 iteration cycles per expression that involves nuanced eye states.
