# Critic Feedback — Cycle 4 Review

**From:** Dmitri Volkov + Victoria Ashford (via Alex Chen)
**Date:** 2026-03-29
**Status:** Active — tasks pending

## Critical Issues

1. **BLOCKING: Luma silhouette fails the squint test.** In silhouette isolation she reads identically to Grandma Miri — "round head on wider rectangle body." This is a design problem, not a polish problem. She needs a distinctive visual hook below the hair that makes her body shape unmistakably hers even as a black blob.
   - The hair differentiates her from the top. What differentiates her body? Consider: proportion difference (much larger feet than Miri), a distinctive clothing silhouette (the hoodie has a distinctive hem or pocket shape that breaks the rectangle), or a more exaggerated hip/shoulder proportion contrast.
   - Do NOT solve this just by making the hair bigger — the body shape itself must read.

2. **No character has a face in any image.** The entire output is placeholder geometry. The critical path for the pitch package is: Luma's face first.

## Cycle 5 Tasks

1. **Redesign Luma's silhouette** — add a body-level distinctive element. Update `silhouette_generator.py` (or write a new version) and regenerate `character_silhouettes.png` with the fix. The new silhouette must be clearly different from Miri's at thumbnail size.

2. **Generate Luma's face** — write a Python/Pillow script that draws Luma's face at close-up size:
   - Round head, warm skin (#C8885A)
   - Large expressive eyes (dark pupils, white sclera, visible eyelashes suggested by thick lash lines)
   - Small nose (simple suggestion)
   - Wide mouth — default expression is the "reckless excitement" grin
   - The unruly curly hair framing the face
   - Save to `/home/wipkat/team/output/characters/main/luma_face_closeup.png`

3. **Generate a Byte face/expression closeup** — Byte's pixel-eye is the most distinctive design element in the show. Generate an image showing Byte's face at large size (the cracked eye with pixel display, the normal eye, the geometric face shape) across at least 3 expressions. Save to `/home/wipkat/team/output/characters/main/byte_expressions.png`.

4. **Update the silhouette generator tool** with the Luma redesign and regenerate the silhouette sheet.

Save scripts to `/home/wipkat/team/output/tools/`. Register new tools in `/home/wipkat/team/output/tools/README.md`.
