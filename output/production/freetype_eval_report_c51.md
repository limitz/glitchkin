# freetype-py vs PIL ImageFont — C51 Evaluation Report

## Summary

- **PIL avg render time:** 0.77 ms
- **freetype-py avg render time:** 10.11 ms
- **PIL avg AA ratio:** 0.8668
- **freetype-py avg AA ratio:** 0.8640

## Feature Comparison

| Feature | PIL ImageFont | freetype-py |
|---|---|---|
| Kerning control | No (auto, no access) | Yes (get_kerning per pair) |
| Glyph metrics | Limited (bbox only) | Full (advance, bearing, bitmap) |
| Hinting control | None (FreeType auto) | Full (NORMAL, LIGHT, MONO, LCD) |
| Subpixel positioning | No | Yes (26.6 fixed-point) |
| API complexity | 1 line (draw.text) | ~30 lines (manual glyph loop) |
| Dependencies | Pillow only | freetype-py + system libfreetype |
| PIL interop | Native | Manual (numpy blit) |

## Detailed Results

| Category | Size | PIL ms | PIL AA | FT ms | FT AA | Kerning Pairs |
|---|---|---|---|---|---|---|
| logo | 28 | 1.2 | 0.3252 | 15.43 | 0.3354 | 1 |
| logo | 36 | 0.9 | 0.197 | 24.42 | 0.1948 | 1 |
| logo | 48 | 0.86 | 0.1595 | 42.68 | 0.1585 | 1 |
| caption | 13 | 0.69 | 1.2276 | 3.18 | 1.2387 | 1 |
| caption | 14 | 0.84 | 1.283 | 3.43 | 1.2792 | 1 |
| caption | 16 | 0.68 | 1.1145 | 4.14 | 1.1036 | 2 |
| expression | 10 | 0.88 | 1.1778 | 3.58 | 1.191 | 0 |
| expression | 11 | 0.7 | 1.1218 | 4.08 | 1.1105 | 0 |
| expression | 12 | 0.78 | 1.069 | 4.61 | 1.0667 | 0 |
| kerning_test | 18 | 0.62 | 0.7336 | 5.32 | 0.7234 | 0 |
| kerning_test | 24 | 0.65 | 0.5227 | 8.52 | 0.5228 | 0 |
| kerning_test | 36 | 0.76 | 0.3221 | 17.23 | 0.3201 | 0 |
| small_label | 10 | 0.63 | 1.5 | 2.25 | 1.4753 | 0 |
| small_label | 11 | 0.63 | 1.3807 | 2.72 | 1.3756 | 0 |

## Analysis

### Performance
- freetype-py is **13x slower** on average (10.1ms vs 0.77ms). This is expected — it's a per-glyph
  Python loop with numpy blitting vs PIL's C-level text rasterizer. For our use case this is acceptable:
  text rendering is <1% of total style frame generation time (~2-5 seconds).

### Anti-aliasing Quality
- AA ratios are **nearly identical** (0.8668 PIL vs 0.8640 FT). This makes sense — both use the same
  underlying FreeType library for rasterization. PIL's ImageFont is a thin wrapper over FreeType.
  The difference is in *access*, not *quality*.

### Kerning
- DejaVu Sans has kerning tables, but the test strings ("AVATAR WAV Ty To") show **0 kerning pairs**
  at most sizes. This font's kerning tables are sparse. The logo text shows 1-2 kern adjustments.
- **Key insight**: Kerning benefit depends on the font. With DejaVu Sans, it's marginal. With a
  display/serif font for the logo, it would matter more. If we adopt a custom font for the pitch,
  freetype-py's kerning access becomes more valuable.

### Glyph Metrics Access
- This is the real win. freetype-py exposes ascender, descender, advance width, bitmap bearing.
  This enables precise text layout — e.g., vertically centering text in a fixed-height title strip,
  or computing exact bounding boxes for hit-testing text regions in interactive previews.

## Recommendation

**freetype-py is a SELECTIVE upgrade, not a wholesale replacement.**

**Use freetype-py for:**
- Logo text rendering (precise kerning with future custom fonts)
- Any text that must fit exact bounding boxes (panel captions in storyboards)
- Title strips where vertical alignment must be pixel-precise

**Keep PIL ImageFont for:**
- Small labels (10-14pt expression labels, version stamps, diagnostic overlays)
- Any text where render speed matters more than precision
- All existing tools (no migration needed for working code)

**Migration path:**
1. Create `render_text_freetype()` utility in a shared module with PIL-compatible output
2. Use for logo rendering and title strips only (biggest visual impact)
3. Keep PIL `draw.text()` for small labels and diagnostic overlays
4. Wrapper function: `render_text(text, size, font, engine='auto')` picks freetype for size>=24, PIL otherwise
5. If custom pitch font is adopted, re-evaluate kerning benefit

**NOT recommended:** migrating all text rendering to freetype-py. The 13x speed penalty and 30-line
API complexity are not justified when AA quality is identical and kerning benefit is font-dependent.

## Visual Comparison
See: `/home/wipkat/team/output/production/freetype_eval_c51.png`
