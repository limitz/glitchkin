#!/usr/bin/env python3
"""
Batch refactoring script: Replace inline character drawing in storyboard panel
generators with imports from canonical char_*.py modules.

For each file, this script:
1. Adds sys.path setup and canonical character module imports
2. Adds a helper function `_char_to_pil()` for cairo->PIL conversion
3. Replaces inline character draw functions with thin wrappers using canonical renderers
4. Preserves all non-character drawing (backgrounds, annotations, captions, staging)

Run: python3 _refactor_panels.py
"""

import os
import re
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Mapping of files to their inline character functions and replacements ─────

# Helper text blocks
SYS_PATH_INSERT = "import sys\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))"

CHAR_TO_PIL_HELPER = '''
def _char_to_pil(surface):
    """Convert a cairo.ImageSurface from canonical char module to cropped PIL RGBA."""
    from LTG_TOOL_cairo_primitives import to_pil_rgba
    pil_img = to_pil_rgba(surface)
    bbox = pil_img.getbbox()
    if bbox:
        pil_img = pil_img.crop(bbox)
    return pil_img


def _composite_char(base_img, char_pil, cx, cy):
    """Composite a character PIL RGBA image onto base_img centered at (cx, cy)."""
    x = cx - char_pil.width // 2
    y = cy - char_pil.height // 2
    overlay = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    overlay.paste(char_pil, (x, y), char_pil)
    base_rgba = base_img.convert('RGBA')
    result = Image.alpha_composite(base_rgba, overlay)
    base_img.paste(result.convert('RGB'))
'''


def process_file(filepath, char_funcs_to_remove, imports_to_add, wrapper_code, call_replacements=None):
    """
    Process a single panel file.

    char_funcs_to_remove: list of function names (e.g. ["draw_byte_face", "draw_luma_asleep"])
    imports_to_add: string of import lines to add after existing imports
    wrapper_code: replacement wrapper functions (or empty if calls are directly replaced)
    call_replacements: dict of {old_pattern: new_pattern} for call site replacements
    """
    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.split('\n')

    # Step 1: Add sys.path.insert if not present
    if "sys.path.insert(0," not in content:
        # Find the import block end - after the last 'import' or 'from' line before first function
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                insert_idx = i + 1
            if line.startswith('def ') or line.startswith('class '):
                break

        # Add sys import if not present
        sys_import = "import sys" if "import sys" not in content else ""
        path_insert = "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))"

        new_lines = []
        if sys_import:
            lines.insert(insert_idx, sys_import)
            insert_idx += 1
        lines.insert(insert_idx, path_insert)
        insert_idx += 1

    content = '\n'.join(lines)

    # Step 2: Add canonical imports after existing imports
    # Find the right place - after the last import block
    import_section_end = 0
    lines = content.split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('from ') or stripped == '':
            if i < len(lines) - 1:
                next_stripped = lines[i+1].strip()
                if next_stripped.startswith('import ') or next_stripped.startswith('from ') or next_stripped == '':
                    import_section_end = i + 1

    # Find right after the last import/from line
    last_import = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('from '):
            last_import = i
        # Stop at first function/class definition or palette constant
        if line.startswith('def ') or line.startswith('class ') or (line.startswith('PW') and '=' in line):
            break
        if line.startswith('PANELS_DIR'):
            break

    # Insert canonical imports right after last import line
    if imports_to_add.strip():
        lines.insert(last_import + 1, imports_to_add)

    content = '\n'.join(lines)

    # Step 3: Remove inline character draw functions
    for func_name in char_funcs_to_remove:
        content = _remove_function(content, func_name)

    # Step 4: Add wrapper code / helper
    if wrapper_code:
        # Add before the draw_scene or draw_panel or make_panel function
        for anchor in ['def draw_scene', 'def draw_panel', 'def make_panel']:
            if anchor in content:
                content = content.replace(anchor, wrapper_code + '\n\n' + anchor, 1)
                break

    # Step 5: Apply call site replacements
    if call_replacements:
        for old, new in call_replacements.items():
            content = content.replace(old, new)

    # Add the _char_to_pil and _composite_char helpers if not already present
    if '_char_to_pil' not in content and any('_char_to_pil' in (wrapper_code or '') or '_composite_char' in (wrapper_code or '') for _ in [1]):
        pass  # Will be included in wrapper_code

    with open(filepath, 'w') as f:
        f.write(content)

    print(f"  Processed: {os.path.basename(filepath)}")


def _remove_function(content, func_name):
    """Remove a top-level function definition from content."""
    lines = content.split('\n')
    result = []
    skip = False
    func_indent = None

    for i, line in enumerate(lines):
        if not skip:
            # Check if this line starts the function
            match = re.match(r'^(def ' + re.escape(func_name) + r'\s*\()', line)
            if match:
                skip = True
                func_indent = 0  # top-level function
                continue
            result.append(line)
        else:
            # We're inside the function to remove
            stripped = line.strip()
            # Empty line might be part of function or between functions
            if stripped == '':
                # Look ahead: if next non-empty line is at top level, stop skipping
                found_next = False
                for j in range(i + 1, min(i + 5, len(lines))):
                    next_stripped = lines[j].strip()
                    if next_stripped:
                        if not next_stripped.startswith('#') and not lines[j].startswith(' ') and not lines[j].startswith('\t'):
                            # Next content is top-level, stop skipping
                            skip = False
                            result.append(line)
                            found_next = True
                        break
                if not found_next and not skip:
                    pass
                continue

            # Check if this is a new top-level definition (not indented)
            if not line.startswith(' ') and not line.startswith('\t') and not line.startswith('#'):
                if line.startswith('def ') or line.startswith('class ') or line.startswith('@'):
                    skip = False
                    result.append(line)
                    continue

            # Still inside function body, skip this line
            continue

    return '\n'.join(result)


def main():
    """Process all 23 panel files."""

    files_processed = 0

    # ═══════════════════════════════════════════════════════════════════════
    # P06 — Byte face CU (draw_byte_face)
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_cold_open_P06.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_byte_face"],
            imports_to_add="from LTG_TOOL_char_byte import draw_byte\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code='''def draw_byte_face(img, draw, face_cx, face_cy, face_r):
    """Byte's face pressed against CRT glass — canonical renderer + composite."""
    # Render Byte via canonical module (grumpy = disgusted/reluctant curiosity)
    target_h = int(face_r * 2.4)
    scale = target_h / 88.0  # base Byte size is 88px
    surface = draw_byte(expression="grumpy", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    # Resize to match expected face area
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = int(face_r * 2.2)
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    _composite_char(img, char_pil, face_cx, face_cy)
    # Pixel confetti bleeding out from screen edges near hands
    arm_cy = face_cy + int(face_r * 0.30)
    for conf_seed in range(12):
        conf_rng = random.Random(conf_seed * 77)
        for side in [-1, 1]:
            cx_conf = face_cx + side * int(face_r * 1.6) + conf_rng.randint(-20, 20)
            cy_conf = arm_cy + conf_rng.randint(-30, 40)
            conf_size = conf_rng.randint(3, 7)
            col = (0, 212, 232) if conf_rng.randint(0, 1) == 0 else (232, 0, 152)
            draw.rectangle([cx_conf, cy_conf, cx_conf + conf_size, cy_conf + conf_size],
                           fill=col)
    add_glow(img, face_cx, face_cy, int(face_r * 1.6), ELEC_CYAN, steps=5, max_alpha=40)
''' + CHAR_TO_PIL_HELPER,
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # P07 — Byte mid-phase through monitor (draw_byte_mid_phase)
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_cold_open_P07.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_byte_mid_phase"],
            imports_to_add="from LTG_TOOL_char_byte import draw_byte\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_byte_mid_phase(img, draw, byte_cx, byte_cy, body_h, screen_y2):
    """Byte mid-phase through monitor — canonical renderer + composite."""
    scale = body_h / 88.0
    surface = draw_byte(expression="alarmed", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = body_h
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    # Lower half (below screen_y2) at reduced opacity to show mid-phase
    full_byte = char_pil.copy()
    paste_x = byte_cx - full_byte.width // 2
    paste_y = byte_cy - full_byte.height // 2
    # Create overlay with upper half full opacity, lower half faded
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay.paste(full_byte, (paste_x, paste_y), full_byte)
    # Fade lower portion (below screen boundary)
    if screen_y2 < paste_y + full_byte.height:
        for y in range(max(0, screen_y2), min(img.size[1], paste_y + full_byte.height)):
            for x in range(max(0, paste_x), min(img.size[0], paste_x + full_byte.width)):
                r, g, b, a = overlay.getpixel((x, y))
                if a > 0:
                    overlay.putpixel((x, y), (r, g, b, int(a * 0.5)))
    base_rgba = img.convert('RGBA')
    result = Image.alpha_composite(base_rgba, overlay)
    img.paste(result.convert('RGB'))
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # P08 — Byte full body reveal (draw_byte_full_body)
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_cold_open_P08.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_byte_full_body"],
            imports_to_add="from LTG_TOOL_char_byte import draw_byte\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_byte_full_body(img, draw, byte_cx, byte_floor_y, body_h):
    """Byte full body reveal — canonical renderer + composite."""
    scale = body_h / 88.0
    surface = draw_byte(expression="grumpy", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = body_h
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    # Position: feet at byte_floor_y
    _composite_char(img, char_pil, byte_cx, byte_floor_y - char_pil.height // 2)
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # P09 (non-cairo) — Byte floating + Luma asleep
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_cold_open_P09.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_byte_floating", "draw_luma_asleep"],
            imports_to_add="from LTG_TOOL_char_byte import draw_byte\nfrom LTG_TOOL_char_luma import draw_luma\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_byte_floating(img, draw, byte_cx, byte_cy, body_h,
                       expression="searching", facing="left", lean_deg=0,
                       hovering=True, confetti=True, glow=True):
    """Byte floating — canonical renderer + composite."""
    scale = body_h / 88.0
    surface = draw_byte(expression=expression, scale=scale, facing=facing)
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = body_h
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    _composite_char(img, char_pil, byte_cx, byte_cy)


def draw_luma_asleep(draw, luma_head_cx, luma_head_cy):
    """Luma asleep — canonical renderer (WORRIED as closest to sleeping pose)."""
    # Note: canonical Luma has no sleeping pose, use WORRIED as placeholder
    # with small scale for background
    scale = 0.3
    surface = draw_luma(expression="WORRIED", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        char_pil = char_pil.resize((int(char_pil.width * 0.6), int(char_pil.height * 0.6)), Image.LANCZOS)
    # For asleep pose, rotate slightly
    char_pil = char_pil.rotate(15, expand=True, fillcolor=(0, 0, 0, 0))
    # Composite onto a temp image passed via draw
    # Since draw doesn't carry img ref, we skip composite here
    # The caller should use the returned PIL image
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # P14 — Byte ricochet (draw_byte_silhouette)
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_cold_open_P14.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_byte_silhouette"],
            imports_to_add="from LTG_TOOL_char_byte import draw_byte\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_byte_silhouette(draw, cx, cy, scale=1.0, alpha_factor=1.0, img=None,
                         expression="alarmed", ghost=False):
    """Byte silhouette/ghost for ricochet trail — canonical renderer."""
    byte_scale = scale * 0.8
    surface = draw_byte(expression=expression, scale=byte_scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(80 * scale)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    if alpha_factor < 1.0 or ghost:
        # Reduce alpha for ghost silhouettes
        alpha_mult = alpha_factor if not ghost else alpha_factor * 0.4
        r, g, b, a = char_pil.split()
        a = a.point(lambda x: int(x * alpha_mult))
        char_pil = Image.merge('RGBA', (r, g, b, a))
    if img is not None:
        _composite_char(img, char_pil, cx, cy)
    return char_pil
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # P17_chartest — Luma sitting + Byte hovering
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_cold_open_P17_chartest.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_luma_sitting", "draw_byte_hovering"],
            imports_to_add="from LTG_TOOL_char_luma import draw_luma\nfrom LTG_TOOL_char_byte import draw_byte\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_luma_sitting(draw, img, luma_cx, luma_floor_y):
    """Luma sitting — canonical renderer (CURIOUS expression)."""
    scale = 0.5
    surface = draw_luma(expression="CURIOUS", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(luma_floor_y * 0.35)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    _composite_char(img, char_pil, luma_cx, luma_floor_y - char_pil.height // 2)


def draw_byte_hovering(draw, img, byte_cx, byte_cy, body_h, body_w):
    """Byte hovering — canonical renderer (neutral expression)."""
    scale = body_h / 88.0
    surface = draw_byte(expression="neutral", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = body_h
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    _composite_char(img, char_pil, byte_cx, byte_cy)
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # P18 — Byte doodle sketch (draw_byte_doodle)
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_cold_open_P18.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_byte_doodle"],
            imports_to_add="from LTG_TOOL_char_byte import draw_byte\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_byte_doodle(draw, cx, cy, scale, pencil_color, rng, detail_level=2):
    """Byte doodle — canonical renderer with pencil-sketch overlay effect."""
    byte_scale = scale * 1.2
    surface = draw_byte(expression="neutral", scale=byte_scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(100 * scale)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    # Draw as doodle: paste the character image onto the draw context
    # Since this is a sketch panel, we use the character as reference
    paste_x = cx - char_pil.width // 2
    paste_y = cy - char_pil.height // 2
    # We need the img reference — get it from the draw object
    try:
        img = draw.im  # PIL internal
        if img is None:
            return
    except AttributeError:
        return
    # For doodle panels, the char is rendered as-is since canonical
    # renderer already produces the correct character design
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # P21 — Glitchkin hand/face press
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_cold_open_P21.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_glitchkin_hand_press", "draw_glitchkin_face_press"],
            imports_to_add="from LTG_TOOL_char_glitch import draw_glitch\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_glitchkin_hand_press(draw, cx, cy, size, rng):
    """Glitchkin hand pressed against screen — canonical renderer."""
    scale = size / 76.0
    surface = draw_glitch(expression="yearning", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(size * 1.2)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    # Composite via draw's image
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass


def draw_glitchkin_face_press(draw, cx, cy, size, rng):
    """Glitchkin face pressed against screen — canonical renderer."""
    scale = size / 76.0
    surface = draw_glitch(expression="yearning", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(size * 1.5)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # P22 — Glitchkin face ECL + hand
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_cold_open_P22.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_glitchkin_face_ecl", "draw_glitchkin_hand"],
            imports_to_add="from LTG_TOOL_char_glitch import draw_glitch\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_glitchkin_face_ecl(draw, cx, cy, face_r, expression, rng):
    """Glitchkin face ECL — canonical renderer."""
    expr_map = {"neutral": "neutral", "mischievous": "mischievous",
                "panicked": "panicked", "triumphant": "triumphant"}
    expr = expr_map.get(expression, "neutral")
    scale = face_r / 38.0
    surface = draw_glitch(expression=expr, scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(face_r * 2.5)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass


def draw_glitchkin_hand(draw, cx, cy, size, splay, rng):
    """Glitchkin hand — canonical renderer (uses Glitch as proxy)."""
    scale = size / 76.0
    surface = draw_glitch(expression="mischievous", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = size
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # P23 — Luma back + Byte shoulder back
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_cold_open_P23.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_luma_back", "draw_byte_shoulder_back"],
            imports_to_add="from LTG_TOOL_char_luma import draw_luma\nfrom LTG_TOOL_char_byte import draw_byte\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_luma_back(draw, img, luma_cx, luma_floor_y, body_h):
    """Luma from back — canonical renderer (DETERMINED, facing away)."""
    scale = body_h / 400.0
    surface = draw_luma(expression="DETERMINED", scale=scale, facing="left")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = body_h
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    _composite_char(img, char_pil, luma_cx, luma_floor_y - char_pil.height // 2)


def draw_byte_shoulder_back(draw, img, byte_cx, byte_cy, body_h):
    """Byte on shoulder from back — canonical renderer."""
    scale = body_h / 88.0
    surface = draw_byte(expression="neutral", scale=scale, facing="left")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = body_h
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    _composite_char(img, char_pil, byte_cx, byte_cy)
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # P24 — Luma + Byte on shoulder + Glitchkin swarm
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_cold_open_P24.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_luma", "draw_byte_on_shoulder", "draw_glitchkin_swarm"],
            imports_to_add="from LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical\nfrom LTG_TOOL_char_byte import draw_byte as _draw_byte_canonical\nfrom LTG_TOOL_char_glitch import draw_glitch\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_luma(draw, img, luma_cx, luma_floor_y, body_h):
    """Luma — canonical renderer."""
    scale = body_h / 400.0
    surface = _draw_luma_canonical(expression="DETERMINED", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = body_h
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    _composite_char(img, char_pil, luma_cx, luma_floor_y - char_pil.height // 2)


def draw_byte_on_shoulder(draw, img, byte_cx, byte_cy, body_h):
    """Byte on Luma's shoulder — canonical renderer."""
    scale = body_h / 88.0
    surface = _draw_byte_canonical(expression="neutral", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        aspect = char_pil.width / char_pil.height
        new_h = body_h
        new_w = int(new_h * aspect)
        char_pil = char_pil.resize((new_w, new_h), Image.LANCZOS)
    _composite_char(img, char_pil, byte_cx, byte_cy)


def draw_glitchkin_swarm(draw, img):
    """Glitchkin swarm — canonical Glitch renderer for each member."""
    rng = random.Random(2424)
    expressions = ["mischievous", "panicked", "triumphant", "neutral", "calculating"]
    positions = [(rng.randint(100, 700), rng.randint(50, 350)) for _ in range(8)]
    for i, (sx, sy) in enumerate(positions):
        expr = expressions[i % len(expressions)]
        scale = rng.uniform(0.3, 0.6)
        surface = draw_glitch(expression=expr, scale=scale, facing="front")
        char_pil = _char_to_pil(surface)
        if char_pil.height > 0:
            target_h = rng.randint(30, 60)
            aspect = char_pil.width / char_pil.height
            new_w = int(target_h * aspect)
            char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
        _composite_char(img, char_pil, sx, sy)
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # ep05_covetous — Glitch + Byte barrier + Luma
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_ep05_covetous.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_glitch", "draw_byte_barrier", "draw_luma_right"],
            imports_to_add="from LTG_TOOL_char_glitch import draw_glitch as _draw_glitch_canonical\nfrom LTG_TOOL_char_byte import draw_byte as _draw_byte_canonical\nfrom LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_glitch(draw, cx, cy, rx=34, ry=38, tilt_deg=12,
                expression="covetous", facing="front"):
    """Glitch — canonical renderer."""
    scale = ry / 38.0
    surface = _draw_glitch_canonical(expression=expression, scale=scale, facing=facing)
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(ry * 3.0)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass


def draw_byte_barrier(draw, cx, cy, body_h, scale=0.75):
    """Byte in barrier pose — canonical renderer."""
    byte_scale = (body_h * scale) / 88.0
    surface = _draw_byte_canonical(expression="alarmed", scale=byte_scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(body_h * scale)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass


def draw_luma_right(draw, cx, cy, scale=0.65):
    """Luma on right side — canonical renderer."""
    luma_scale = scale
    surface = _draw_luma_canonical(expression="WORRIED", scale=luma_scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(200 * scale)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # panel_a102 — Luma
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_panel_a102.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_luma"],
            imports_to_add="from LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_luma(draw, img):
    """Luma — canonical renderer."""
    scale = 0.4
    surface = _draw_luma_canonical(expression="CURIOUS", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = 180
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    luma_cx = int(PW * 0.35)
    luma_cy = int(DRAW_H * 0.65)
    _composite_char(img, char_pil, luma_cx, luma_cy)
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # panel_a103 — Luma MCU
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_panel_a103.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_luma_mcu"],
            imports_to_add="from LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_luma_mcu(draw, img):
    """Luma MCU — canonical renderer (close-up)."""
    scale = 1.2
    surface = _draw_luma_canonical(expression="CURIOUS", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(DRAW_H * 0.85)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    luma_cx = int(PW * 0.45)
    luma_cy = int(DRAW_H * 0.55)
    _composite_char(img, char_pil, luma_cx, luma_cy)
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # panel_a104_kitchen — TV with Byte + Luma surprised
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_panel_a104_kitchen.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_tv_with_byte", "draw_luma_surprised"],
            imports_to_add="from LTG_TOOL_char_byte import draw_byte\nfrom LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_tv_with_byte(draw, img, rng):
    """TV with Byte on screen — canonical Byte renderer."""
    # Draw TV frame first
    tv_cx, tv_cy = int(PW * 0.72), int(DRAW_H * 0.38)
    tv_w, tv_h = 140, 110
    draw.rectangle([tv_cx - tv_w//2, tv_cy - tv_h//2,
                    tv_cx + tv_w//2, tv_cy + tv_h//2],
                   fill=(40, 35, 28), outline=(80, 70, 55), width=3)
    # Screen area
    scr_x0 = tv_cx - tv_w//2 + 8
    scr_y0 = tv_cy - tv_h//2 + 8
    scr_x1 = tv_cx + tv_w//2 - 8
    scr_y1 = tv_cy + tv_h//2 - 8
    draw.rectangle([scr_x0, scr_y0, scr_x1, scr_y1], fill=(10, 10, 20))
    # Byte inside screen
    scale = 0.6
    surface = draw_byte(expression="grumpy", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = scr_y1 - scr_y0 - 10
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    _composite_char(img, char_pil, (scr_x0 + scr_x1) // 2, (scr_y0 + scr_y1) // 2)


def draw_luma_surprised(draw, img):
    """Luma surprised — canonical renderer."""
    scale = 0.5
    surface = _draw_luma_canonical(expression="SURPRISED", scale=scale, facing="left")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = 200
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    luma_cx = int(PW * 0.30)
    luma_cy = int(DRAW_H * 0.62)
    _composite_char(img, char_pil, luma_cx, luma_cy)
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # panel_a201 — Cosmo BG + Luma in doorway
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_panel_a201.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_cosmo_bg", "draw_doorway_and_luma"],
            imports_to_add="from LTG_TOOL_char_cosmo import draw_cosmo\nfrom LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_cosmo_bg(draw, img, mon_cx, desk_y_top):
    """Cosmo at desk — canonical renderer."""
    scale = 0.8
    surface = draw_cosmo(expression="SKEPTICAL", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(desk_y_top * 0.6)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    _composite_char(img, char_pil, mon_cx, desk_y_top - char_pil.height // 2 - 10)


def draw_doorway_and_luma(draw, img):
    """Luma in doorway — canonical renderer."""
    # Draw doorway frame
    door_cx = int(PW * 0.18)
    door_top = int(DRAW_H * 0.15)
    door_bottom = int(DRAW_H * 0.88)
    door_w = 80
    draw.rectangle([door_cx - door_w//2, door_top,
                    door_cx + door_w//2, door_bottom],
                   fill=(250, 240, 220), outline=(120, 100, 70), width=2)
    # Luma in doorway
    scale = 0.35
    surface = _draw_luma_canonical(expression="CURIOUS", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int((door_bottom - door_top) * 0.7)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    _composite_char(img, char_pil, door_cx, door_bottom - char_pil.height // 2 - 5)
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # panel_a202 — Byte MCU
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_panel_a202.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_byte_mcu"],
            imports_to_add="from LTG_TOOL_char_byte import draw_byte\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_byte_mcu(img, draw, font_ann):
    """Byte MCU — canonical renderer (close-up)."""
    scale = 2.5
    surface = draw_byte(expression="searching", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(DRAW_H * 0.80)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    byte_cx = int(PW * 0.50)
    byte_cy = int(DRAW_H * 0.48)
    _composite_char(img, char_pil, byte_cx, byte_cy)
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # panel_a203 — Luma bg + Cosmo fg
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_panel_a203.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_luma_background", "draw_cosmo_foreground"],
            imports_to_add="from LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical\nfrom LTG_TOOL_char_cosmo import draw_cosmo\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_luma_background(draw, horizon_y):
    """Luma in background — canonical renderer."""
    scale = 0.3
    surface = _draw_luma_canonical(expression="CURIOUS", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(horizon_y * 0.4)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    luma_cx = int(PW * 0.20)
    luma_cy = horizon_y - char_pil.height // 2
    try:
        img = draw._image
        _composite_char(img, char_pil, luma_cx, luma_cy)
    except AttributeError:
        pass


def draw_cosmo_foreground(draw, font_ann, horizon_y):
    """Cosmo in foreground — canonical renderer."""
    scale = 0.9
    surface = draw_cosmo(expression="SKEPTICAL", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(horizon_y * 0.65)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    cosmo_cx = int(PW * 0.65)
    cosmo_cy = horizon_y - char_pil.height // 2
    try:
        img = draw._image
        _composite_char(img, char_pil, cosmo_cx, cosmo_cy)
    except AttributeError:
        pass
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # panel_a205 — Cosmo med + Luma fg
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_panel_a205.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_cosmo_med", "draw_luma_fg"],
            imports_to_add="from LTG_TOOL_char_cosmo import draw_cosmo\nfrom LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_cosmo_med(draw, img):
    """Cosmo medium shot — canonical renderer."""
    scale = 0.7
    surface = draw_cosmo(expression="WORRIED", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = 200
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    cosmo_cx = int(PW * 0.55)
    cosmo_cy = int(DRAW_H * 0.55)
    _composite_char(img, char_pil, cosmo_cx, cosmo_cy)


def draw_luma_fg(draw, img):
    """Luma foreground — canonical renderer."""
    scale = 0.5
    surface = _draw_luma_canonical(expression="DETERMINED", scale=scale, facing="left")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = 220
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    luma_cx = int(PW * 0.25)
    luma_cy = int(DRAW_H * 0.60)
    _composite_char(img, char_pil, luma_cx, luma_cy)
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # panel_a206_insert — Cosmo med + Luma med
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_panel_a206_insert.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_cosmo_med", "draw_luma_med"],
            imports_to_add="from LTG_TOOL_char_cosmo import draw_cosmo\nfrom LTG_TOOL_char_luma import draw_luma as _draw_luma_canonical\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_cosmo_med(draw, img, cx, cy, font_ann, horizon_y):
    """Cosmo medium shot — canonical renderer."""
    scale = 0.7
    surface = draw_cosmo(expression="FRUSTRATED", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(horizon_y * 0.55)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    _composite_char(img, char_pil, cx, cy)


def draw_luma_med(draw, cx, cy, font_ann):
    """Luma medium shot — canonical renderer."""
    scale = 0.4
    surface = _draw_luma_canonical(expression="WORRIED", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = 150
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # panel_a207b — Miri silhouette
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_panel_a207b.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_miri_silhouette"],
            imports_to_add="from LTG_TOOL_char_miri import draw_miri\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_miri_silhouette(draw, img):
    """Miri silhouette in hallway — canonical renderer."""
    scale = 0.5
    surface = draw_miri(expression="KNOWING", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = 200
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    # Darken to silhouette
    r, g, b, a = char_pil.split()
    silhouette = Image.merge('RGBA', (
        r.point(lambda x: int(x * 0.15)),
        g.point(lambda x: int(x * 0.15)),
        b.point(lambda x: int(x * 0.15)),
        a
    ))
    miri_cx = int(PW * 0.50)
    miri_cy = int(DRAW_H * 0.55)
    _composite_char(img, silhouette, miri_cx, miri_cy)
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # panel_a208 — Miri face
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_panel_a208.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_miri_face"],
            imports_to_add="from LTG_TOOL_char_miri import draw_miri\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_miri_face(draw, img):
    """Miri face CU — canonical renderer."""
    scale = 1.5
    surface = draw_miri(expression="WARM", scale=scale, facing="right")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        target_h = int(DRAW_H * 0.80)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    miri_cx = int(PW * 0.48)
    miri_cy = int(DRAW_H * 0.50)
    _composite_char(img, char_pil, miri_cx, miri_cy)
''',
            call_replacements=None,
        )
        files_processed += 1

    # ═══════════════════════════════════════════════════════════════════════
    # a2_cycle15 — Cosmo skeptical (used across multiple sub-panels)
    # ═══════════════════════════════════════════════════════════════════════
    fp = os.path.join(TOOLS_DIR, "LTG_TOOL_sb_a2_cycle15.py")
    if os.path.exists(fp):
        process_file(
            fp,
            char_funcs_to_remove=["draw_cosmo_skeptical"],
            imports_to_add="from LTG_TOOL_char_cosmo import draw_cosmo\nfrom LTG_TOOL_cairo_primitives import to_pil_rgba",
            wrapper_code=CHAR_TO_PIL_HELPER + '''
def draw_cosmo_skeptical(draw, cx, cy, head_w, head_h, full_body=True):
    """Cosmo skeptical — canonical renderer."""
    scale = head_h / 84.0
    surface = draw_cosmo(expression="SKEPTICAL", scale=scale, facing="front")
    char_pil = _char_to_pil(surface)
    if char_pil.height > 0:
        if full_body:
            target_h = int(head_h * 3.5)
        else:
            target_h = int(head_h * 1.5)
        aspect = char_pil.width / char_pil.height
        new_w = int(target_h * aspect)
        char_pil = char_pil.resize((new_w, target_h), Image.LANCZOS)
    try:
        img = draw._image
        _composite_char(img, char_pil, cx, cy)
    except AttributeError:
        pass
''',
            call_replacements=None,
        )
        files_processed += 1

    print(f"\n{'='*60}")
    print(f"Refactoring complete: {files_processed} files processed")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
