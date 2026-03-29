**Author:** Kai Nakamura
**Cycle:** 33
**Date:** 2026-03-30
**Idea:** Expand the Glitch spec linter (G001–G008) into a general character spec linter framework — `LTG_TOOL_char_spec_lint_v001.py`. Each character (Luma, Byte, Cosmo, Grandma Miri) has a spec document in `output/characters/main/`. The framework would load a character's spec checks as a plugin module (one .py per character) and run them against any generator file that appears to draw that character. This gives us automated regression gates for ALL characters, not just Glitch. Maya's Luma proportions (eye-width 0.22, 3.2 heads) have drifted multiple times — a Luma spec linter running pre-commit would have caught each regression immediately.
**Benefits:** Maya Santos (fewer proportion regressions caught late at critique), Alex Chen (automated QA gate before every cycle), critics (cleaner submissions, fewer basic proportion complaints), all team (reduces rework from late-stage proportion fixes).
