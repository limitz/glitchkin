#!/usr/bin/env python3
# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through AI
# direction and human assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
LTG_TOOL_project_paths.py — Project Root Resolver Utility
"Luma & the Glitchkin" — Technical Art / Kai Nakamura / Cycle 44

Provides `project_root()` — resolves the project root directory at runtime
by traversing parent directories until CLAUDE.md (the project sentinel) is
found.  This eliminates all hardcoded /home/wipkat/team paths across the
toolchain, making every generator portable across machines and deployment
environments.

Usage in generators:
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from LTG_TOOL_project_paths import project_root, output_dir, tools_dir

    # Replace:  OUTPUT_PATH = "/home/wipkat/team/output/backgrounds/..."
    # With:     OUTPUT_PATH = output_dir("backgrounds", "LTG_ENV_foo.png")

Public API:
    project_root()                  -> pathlib.Path  (project root, cached)
    output_dir(*parts)              -> pathlib.Path  (output/ + parts joined)
    tools_dir(*parts)               -> pathlib.Path  (output/tools/ + parts joined)
    ensure_dir(path)                -> pathlib.Path  (mkdir -p, returns path)
    resolve_output(category, name)  -> pathlib.Path  (category subdir + filename)

Migration guide (replace hardcoded paths):
    OLD:  PANELS_DIR = "/home/wipkat/team/output/storyboards/panels"
    NEW:  PANELS_DIR = output_dir("storyboards", "panels")

    OLD:  out_path = "/home/wipkat/team/output/backgrounds/environments/LTG_ENV_foo.png"
    NEW:  out_path = output_dir("backgrounds", "environments", "LTG_ENV_foo.png")

    OLD:  BASE = "/home/wipkat/team/output"
    NEW:  from LTG_TOOL_project_paths import output_dir as BASE_DIR
          # use BASE_DIR("subdir", "file.png") instead of os.path.join(BASE, ...)

    After changing path constants, always call ensure_dir(parent) before save:
          ensure_dir(out_path.parent)

Sentinel file: CLAUDE.md at project root.  If not found in any ancestor,
falls back to the directory two levels above this file's location (i.e.
the directory containing output/tools/ → output/ → project root).

No external dependencies — stdlib pathlib only.
"""

__version__ = "1.0.0"

import pathlib
import functools

_SENTINEL = "CLAUDE.md"   # file present exclusively at project root


# ---------------------------------------------------------------------------
# Core resolver
# ---------------------------------------------------------------------------

@functools.lru_cache(maxsize=1)
def project_root() -> pathlib.Path:
    """Return the project root directory (cached after first call).

    Searches upward from this file's directory for CLAUDE.md.
    Falls back to <this_file>/../.. if sentinel is not found.

    Returns:
        pathlib.Path: Absolute path to the project root directory.

    Raises:
        FileNotFoundError: If fallback directory does not exist on disk.
    """
    start = pathlib.Path(__file__).resolve().parent
    candidate = start
    while True:
        if (candidate / _SENTINEL).exists():
            return candidate
        parent = candidate.parent
        if parent == candidate:
            # Reached filesystem root — use fallback
            fallback = start.parent.parent  # output/tools/ -> output/ -> root
            if fallback.is_dir():
                return fallback
            raise FileNotFoundError(
                f"LTG_TOOL_project_paths: could not locate '{_SENTINEL}' in "
                f"any ancestor of {start}. Fallback {fallback} also not found."
            )
        candidate = parent


# ---------------------------------------------------------------------------
# Convenience helpers
# ---------------------------------------------------------------------------

def output_dir(*parts: str) -> pathlib.Path:
    """Return a path inside the project's output/ directory.

    Args:
        *parts: Path components relative to output/.  May include a filename
                as the final element (no mkdir is performed on the returned path).

    Returns:
        pathlib.Path: Absolute path to output/<parts joined>.

    Example:
        output_dir("backgrounds", "environments", "LTG_ENV_foo.png")
        # → /home/wipkat/team/output/backgrounds/environments/LTG_ENV_foo.png
    """
    return project_root() / "output" / pathlib.Path(*parts) if parts else project_root() / "output"


def tools_dir(*parts: str) -> pathlib.Path:
    """Return a path inside the project's output/tools/ directory.

    Args:
        *parts: Path components relative to output/tools/.

    Returns:
        pathlib.Path: Absolute path to output/tools/<parts joined>.
    """
    return output_dir("tools", *parts) if parts else output_dir("tools")


def ensure_dir(path: pathlib.Path) -> pathlib.Path:
    """Create directory (and parents) if it does not exist.  Returns path.

    Use this before saving any output file:
        ensure_dir(out_path.parent)
        img.save(out_path)

    Args:
        path (pathlib.Path): Directory to create.

    Returns:
        pathlib.Path: The (now existing) directory path.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def resolve_output(category: str, filename: str) -> pathlib.Path:
    """Resolve a standard LTG output path by category shorthand.

    Category shorthands:
        "backgrounds"  / "bg"  → output/backgrounds/environments/
        "storyboards"  / "sb"  → output/storyboards/panels/
        "style_frames" / "sf"  → output/color/style_frames/
        "characters"   / "ch"  → output/characters/main/
        "color_keys"   / "ck"  → output/color/color_keys/thumbnails/
        "tools"        / "tl"  → output/tools/
        "production"   / "pr"  → output/production/

    For paths not covered by a shorthand, use output_dir() directly.

    Args:
        category (str): Category shorthand or keyword.
        filename (str): Output filename (e.g. "LTG_ENV_foo.png").

    Returns:
        pathlib.Path: Full absolute output path (directory is NOT created).
    """
    _MAP = {
        "backgrounds":  ("backgrounds", "environments"),
        "bg":           ("backgrounds", "environments"),
        "storyboards":  ("storyboards", "panels"),
        "sb":           ("storyboards", "panels"),
        "style_frames": ("color", "style_frames"),
        "sf":           ("color", "style_frames"),
        "characters":   ("characters", "main"),
        "ch":           ("characters", "main"),
        "color_keys":   ("color", "color_keys", "thumbnails"),
        "ck":           ("color", "color_keys", "thumbnails"),
        "tools":        ("tools",),
        "tl":           ("tools",),
        "production":   ("production",),
        "pr":           ("production",),
    }
    parts = _MAP.get(category, (category,))
    return output_dir(*parts, filename)


# ---------------------------------------------------------------------------
# Audit helper — find all hardcoded paths across output/tools/
# ---------------------------------------------------------------------------

def audit_hardcoded_paths(tools_directory=None, pattern="/home/"):
    """Scan all .py files in tools_directory for hardcoded absolute paths.

    Prints a report of offending files + line numbers.  Intended as a
    one-shot migration helper — run once to find all callers, then fix.

    Args:
        tools_directory (str | pathlib.Path | None): Defaults to output/tools/.
        pattern (str): String to search for.  Default "/home/" catches any
                       hardcoded home-directory path regardless of username.

    Returns:
        list[dict]: Each entry has keys: file (str), line (int), text (str).
    """
    if tools_directory is None:
        tools_directory = tools_dir()
    tools_directory = pathlib.Path(tools_directory)
    findings = []
    for py_file in sorted(tools_directory.glob("*.py")):
        try:
            lines = py_file.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, line in enumerate(lines, 1):
            if pattern in line:
                findings.append({
                    "file": py_file.name,
                    "line": lineno,
                    "text": line.rstrip(),
                })
    return findings


# ---------------------------------------------------------------------------
# CLI — audit mode
# ---------------------------------------------------------------------------

def _cli_audit():
    import sys
    findings = audit_hardcoded_paths()
    if not findings:
        print("PASS — no hardcoded /home/ paths found in output/tools/*.py")
        return
    # Group by file
    by_file: dict[str, list] = {}
    for f in findings:
        by_file.setdefault(f["file"], []).append(f)
    print(f"AUDIT — {len(findings)} hardcoded path occurrence(s) in {len(by_file)} file(s)")
    print("=" * 70)
    for fname, hits in sorted(by_file.items()):
        print(f"\n  {fname}  ({len(hits)} hit(s))")
        for h in hits:
            print(f"    L{h['line']:4d}  {h['text'][:80]}")
    print()
    print("Migration: replace hardcoded paths with output_dir() / ensure_dir().")
    print("See LTG_TOOL_project_paths.py module docstring for examples.")
    sys.exit(1)   # non-zero so CI can detect remaining violations


if __name__ == "__main__":
    import sys
    if "--audit" in sys.argv or len(sys.argv) == 1:
        _cli_audit()
    elif "--root" in sys.argv:
        print(project_root())
    elif "--output" in sys.argv:
        print(output_dir())
    elif "--tools" in sys.argv:
        print(tools_dir())
    else:
        print(f"project_root  = {project_root()}")
        print(f"output_dir()  = {output_dir()}")
        print(f"tools_dir()   = {tools_dir()}")
