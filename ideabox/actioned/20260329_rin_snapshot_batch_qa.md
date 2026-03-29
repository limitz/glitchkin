**Author:** Rin Yamamoto
**Cycle:** 34
**Date:** 2026-03-29
**Idea:** Add a `batch_snapshot_qa(img_path, regions_spec, out_dir)` helper that reads a JSON regions spec file (list of {label, region} dicts) and calls `scene_snapshot()` for each entry. Pipeline scripts could ship a `<asset>_qa_regions.json` alongside the generator, and any reviewer could run `python batch_snapshot_qa.py LTG_COLOR_styleframe_X_v006.png` to instantly produce a set of labelled close-ups (face, hands, background detail, logo) without touching the main generator.
**Benefits:** Critics and reviewers get targeted crops automatically without manually describing regions to Claude. Reduces back-and-forth during critique cycles, avoids sending full 1280×720 frames to Claude for face-level review, and makes QA regions an explicit documented artifact alongside each generator.
