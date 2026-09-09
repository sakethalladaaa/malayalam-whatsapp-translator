"""
Phase 7 — Conservative Malayalam post-transliteration normalization.

This module operates only on Malayalam-script output produced by IndicXlit.
It does not modify Roman input, language routing, or the IndicXlit model.

Rules are limited to surface-form corrections supported by frozen Phase 6
failure evidence.
"""

from __future__ import annotations

import re
from typing import Final


# Evidence-backed exact surface-form corrections observed in Phase 6.
NORMALIZATION_RULES: Final[dict[str, str]] = {
    "ഇന്നു": "ഇന്ന്",
    "ഒന്നു": "ഒന്ന്",
    "ചെയ്യു": "ചെയ്യൂ",
    "വിളിക്കം": "വിളിക്കാം",
}


def normalize_malayalam(text: str) -> str:
    """
    Apply conservative Malayalam surface-form normalization.

    Only explicitly registered, evidence-backed surface forms are changed.
    """
    if not text or not text.strip():
        return ""

    normalized = text.strip()

    for source, target in NORMALIZATION_RULES.items():
        if source == "ചെയ്യു":
            normalized = re.sub(
                rf"(?<!\S){re.escape(source)}(?!\S)",
                target,
                normalized,
            )
        else:
            normalized = normalized.replace(source, target)

    return normalized
