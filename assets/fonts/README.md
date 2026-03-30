# Fonts — "Luma & the Glitchkin"

All fonts used in this project are open-source (SIL Open Font License or equivalent).
No proprietary typefaces are permitted.

## Currently Required

| File | Family | Weight | Use | Source |
|---|---|---|---|---|
| `Nunito-Bold.ttf` | Nunito | Bold | "Luma" and "the" in logo | [Google Fonts](https://fonts.google.com/specimen/Nunito) |
| `SpaceGrotesk-Bold.ttf` | Space Grotesk | Bold | "Glitchkin" in logo | [Google Fonts](https://fonts.google.com/specimen/Space+Grotesk) |

## License

Both fonts are licensed under the [SIL Open Font License, Version 1.1](https://openfontlicense.org/).
Full license text: https://openfontlicense.org/open-font-license-official-text/

## Installation (one-time setup)

Download the static TTF files directly from Google Fonts:

1. **Nunito Bold:** https://fonts.google.com/specimen/Nunito
   - Click "Download family" → extract → copy `static/Nunito-Bold.ttf` to this directory
   - Rename to `Nunito-Bold.ttf` if not already named that

2. **Space Grotesk Bold:** https://fonts.google.com/specimen/Space+Grotesk
   - Click "Download family" → extract → copy `static/SpaceGrotesk-Bold.ttf` to this directory
   - Rename to `SpaceGrotesk-Bold.ttf` if not already named that

Or via command line (if wget is available):
```
# Nunito Bold
wget "https://github.com/googlefonts/nunito/raw/main/fonts/ttf/Nunito-Bold.ttf" \
     -O /path/to/assets/fonts/Nunito-Bold.ttf

# Space Grotesk Bold
wget "https://github.com/floriankarsten/space-grotesk/raw/master/fonts/ttf/SpaceGrotesk-Bold.ttf" \
     -O /path/to/assets/fonts/SpaceGrotesk-Bold.ttf
```

## Secondary Candidate (on hold)

- **Raleway ExtraBold + Share Tech Mono** — CRT-terminal concept directly referencing Grandma Miri's television. Held as alternative pitch version candidate. See `output/production/ltg_typography_brief_display_typeface.md` for full rationale.

## Design Decision

**Selected C44 by Alex Chen:** Nunito Bold (Luma / Real World) + Space Grotesk Bold (Glitchkin / Glitch Layer).

Nunito's rounded humanist warmth maps to Luma's character shape language. Space Grotesk's geometric-technical construction maps to the Glitch Layer's pixel DNA without reading as generic developer aesthetic. Both SIL OFL.
