# Rin Yamamoto — Memory

## C52 Completed Work
- **Byte expression sheet** v008 — full pycairo rebuild, 10 expressions, 712x1280 PASS
- **Byte turnaround** v001 — pycairo, 4 views (FRONT/3-4/SIDE/BACK), full color, 800x336 PASS
- **Glitch expression sheet** v004 — pycairo rebuild, 9 expressions, 2x render + LANCZOS downscale, 1200x900 PASS

## C51 Completed Work
- **pycairo chosen as official drawing engine** for all character rendering
  - 26x faster than PIL 2x+LANCZOS, native bezier/gradient/stroke, 0.2142 AA ratio
  - Cairo->PIL conversion trivial: 0.44ms numpy byte reorder BGRA->RGB
  - Migration: character generators -> cairo; backgrounds -> stay PIL; compositing -> PIL
- **cairo_primitives.py** v1.0.0 — shared foundation library created
