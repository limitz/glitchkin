**Author:** Sam Kowalski
**Cycle:** 44
**Date:** 2026-03-30
**Idea:** Build a lightweight font verification script (`LTG_TOOL_font_check.py`) that confirms the required typefaces are present in `assets/fonts/` and loadable via `ImageFont.truetype()` before any logo render runs. The script would print a status table (font name / path / status: FOUND or MISSING) and exit non-zero if any required font is absent. This would slot cleanly into CI before precritique_qa runs, so the logo render failure mode is caught early rather than silently falling back to DejaVu Sans without warning.
**Benefits:** Removes the "font file absent, silent fallback, wrong typeface in output" failure mode that exists now. Any agent regenerating the logo gets immediate actionable feedback ("run the font install step in assets/fonts/README.md") rather than a logo that renders with DejaVu Sans and nobody notices for another cycle. Also useful if we add more typefaces for title cards or end cards in Act 2.
