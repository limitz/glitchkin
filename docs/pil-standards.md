# PIL Coding Standards

## Drawing Context
After **any** `img.paste()`, `sheet.paste()`, `variable_stroke()`, `add_rim_light()`, or `add_face_lighting()` call, immediately refresh the draw context:
```python
draw = ImageDraw.Draw(img)
```
Failure to do this causes subsequent draws to silently go to a stale surface (confirmed production bug W004).

## Versioning
- **Overwrite files in place — git tracks history.** Do not add version suffixes to filenames.
- Use `git commit` after each cycle to snapshot state. History is recoverable via git log.

## Naming
- Tools: `LTG_TOOL_[descriptor].py`
- Output PNGs: `LTG_[CATEGORY]_[descriptor]_[variant].png`
- `output/production/` files: descriptive names only (no LTG prefix required).

## Dependencies
- PIL/Pillow for I/O and drawing
- NumPy and OpenCV (cv2) authorized for array ops and analysis (OpenCV default is BGR — convert on load)
- PyTorch authorized if neural analysis needed
- No cairocffi or other external deps
- All procedural elements must use seeded RNG for reproducibility
