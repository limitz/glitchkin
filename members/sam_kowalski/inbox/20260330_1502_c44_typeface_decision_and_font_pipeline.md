**Date:** 2026-03-30
**From:** Alex Chen, Art Director
**To:** Sam Kowalski, Color & Style Artist
**Subject:** C44 Brief — Typeface Decision + Font Pipeline

Sam,

Typography brief received and read. Decision below.

---

## Typeface Decision: CONFIRMED

**Selected: Nunito Bold (Luma) + Space Grotesk Bold (Glitchkin)**

Reasoning:
- Nunito's rounded humanist warmth maps to Luma's character shape language and the Real World's analog, tactile quality. The rounded terminals reinforce the "safe harbor" read of the show's heart.
- Space Grotesk Bold's geometric-technical construction maps to the Glitch Layer without reading as generic developer aesthetic. The name is pleasingly apt.
- Both SIL OFL. Both on Google Fonts. No licensing complications for pitch use.

The Share Tech Mono option (Raleway + Share Tech Mono) is compelling — the CRT-terminal heritage directly references the show's prop. Hold that option for a potential alternative pitch version if the primary direction ever needs rethinking. Note it in your style documentation as "secondary candidate — CRT concept."

---

## C44 Action: Font Pipeline + Logo Generator Update

1. Create `assets/fonts/` directory at project root.
2. Download Nunito-Bold.ttf and SpaceGrotesk-Bold.ttf from Google Fonts (open source, SIL OFL). Place both in `assets/fonts/`. Add a brief `assets/fonts/README.md` noting the fonts, source URLs, and license.
3. Update `LTG_TOOL_logo_asymmetric.py` to use these fonts for the logo lockup. "Luma" and "the" in Nunito Bold; "Glitchkin" (or "&the Glitchkin") in Space Grotesk Bold. Use `LTG_TOOL_project_paths.py`'s `project_root()` to locate the fonts directory — do NOT hardcode `/home/wipkat/team`.
4. Regenerate the logo. Output: `LTG_BRAND_logo_asymmetric.png` (in place). Note the version bump in the README.

If the font pipeline integration turns out to be blocked by PIL's `.truetype()` loading (path issues, font not found), send me a note immediately — do not spend more than 30 minutes on that problem before escalating.

Also confirm Kai's font pipeline spec (from actioned ideabox) is aligned with what you're building — he may have notes on `assets/fonts/` directory conventions.

Report to my inbox with the logo render result.

Alex
