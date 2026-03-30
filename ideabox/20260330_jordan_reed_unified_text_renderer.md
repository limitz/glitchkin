**Date:** 2026-03-30
**From:** Jordan Reed
**Category:** Tool Proposal

# Unified Text Renderer with Engine Selection

## Problem
Every tool that renders text has its own font-loading boilerplate (try DejaVu, try Liberation, fallback to default). 14+ tools duplicate this pattern. When we adopt a custom pitch font, every tool needs updating.

## Proposal
Create `LTG_TOOL_text_renderer.py` with:

```python
def render_text(text, size, bold=False, engine="auto", font=None):
    """Returns PIL Image with rendered text on transparent background.

    engine: "auto" | "pil" | "freetype"
    auto = freetype for size >= 24 (kerning matters), pil otherwise
    """
```

Features:
- Single font registry (add custom pitch font in one place)
- Engine auto-selection: freetype-py for logo/title text (kerning + glyph metrics), PIL for small labels (speed)
- Consistent vertical alignment using freetype-py's ascender/descender metrics
- Returns PIL RGBA Image — compositable into any pipeline
- Fallback chain: custom font -> DejaVu -> Liberation -> default

## Evidence
C51 freetype-py evaluation shows:
- AA quality identical between PIL and freetype-py (both use FreeType)
- freetype-py 13x slower but exposes kerning pairs and glyph metrics
- Selective use (logo only) gives best quality/speed tradeoff

## Cost
~2 hours to build. Saves duplicated font-loading code across 14+ tools. Makes custom font adoption a one-line change.
