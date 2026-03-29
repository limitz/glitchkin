**Author:** Jordan Reed
**Cycle:** 37
**Date:** 2026-03-30
**Idea:** Add a generator template file (`LTG_TOOL_env_generator_template.py`) to `output/tools/` that serves as a starter scaffold for new environment generators. The template would include the standard imports, argparse block with `--check-warmth` already wired up, the `run_warmth_hook` call at the end, the thumbnail ≤ 1280px line, and comments marking each section (palette constants, drawing functions, main). New artists (like Hana) would copy the template and fill in the scene-specific drawing code without having to hunt through existing generators to learn the expected pattern.
**Benefits:** Hana Okonkwo onboards faster — she gets the `--check-warmth` hook, the image size rule, and the output path convention for free. Reduces the chance of missing these steps on new generators. Also helps future artists joining mid-project who need to produce new environments quickly.
