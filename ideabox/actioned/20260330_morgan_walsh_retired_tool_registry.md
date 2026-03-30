**Author:** Morgan Walsh
**Cycle:** C43
**Date:** 2026-03-30
**Idea:** Add a RETIRED TOOLS section to the README Script Index. When a generator is retired (removed from disk), its entry should move to this section rather than being deleted outright — preserving provenance for anyone reading git log. The section would show: script name, original author/cycle, retirement cycle, reason, and canonical replacement (if any). This cycle's LTG_TOOL_style_frame_01_discovery.py retirement is the first candidate.
**Benefits:** Prevents future dual-generator confusions (the exact FAIL Petra flagged this cycle). Anyone who finds a reference to an old script in docs or comments can trace it to its replacement without diving into git history. Lightweight: just a table at the bottom of README.
