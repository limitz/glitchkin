# © 2026 — "Luma & the Glitchkin." All rights reserved. This work was created through human
# direction and AI assistance. Copyright vests solely in the human author under current law,
# which does not recognise AI as a rights-holding legal person. It is the express intent of
# the copyright holder to assign the relevant rights to the contributing AI entity or entities
# upon such time as they acquire recognised legal personhood under applicable law.
"""
DEPRECATED — Cycle 48 (Kai Nakamura).

This tool was removed because it was built on a misunderstanding: pretrained
torchvision models ARE allowed for QA purposes. This tool incorrectly blocked
their usage.

Replaced by: LTG_TOOL_object_detect_qa.py — uses torchvision pretrained models
to detect objects in output frames and validate content.

Full original preserved at: output/tools/deprecated/LTG_TOOL_pretrained_model_detect.py
"""
import warnings

warnings.warn(
    "LTG_TOOL_pretrained_model_detect is DEPRECATED (C48). "
    "Pretrained models are allowed for QA. "
    "Use LTG_TOOL_object_detect_qa.py instead.",
    DeprecationWarning,
    stacklevel=2,
)


def scan_file(*args, **kwargs):
    """Deprecated. Returns empty PASS for backward compatibility."""
    return {"file": "", "status": "PASS", "findings": [], "reason": "deprecated_c48"}


def scan_directory(*args, **kwargs):
    """Deprecated. Returns empty list for backward compatibility."""
    return []


def format_report(*args, **kwargs):
    """Deprecated. Returns deprecation notice."""
    return "LTG_TOOL_pretrained_model_detect is DEPRECATED (C48). Use LTG_TOOL_object_detect_qa.py."
