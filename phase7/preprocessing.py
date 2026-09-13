"""
Phase 7 — Conservative Roman input and Malayalam output normalization.

Roman input rules come from the Phase 7 development experiment.
Malayalam output rules come from historical Phase 6 failure evidence.
Language routing and the IndicXlit model are unchanged.
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

ROMAN_NORMALIZATION_RULES: Final[dict[str, str]] = {
    "nale": "naale",
    "ariyamo": "ariyaamo",
    "inu": "innu",
}


def normalize_malayalam(text: str) -> str:
    """
    Apply conservative Malayalam surface-form normalization.

    Only explicitly registered, evidence-backed surface forms are changed.
    """
    if not text or not text.strip():
        return ""

    normalized = text.strip()

    # Include Malayalam combining marks and joiners in token boundaries.
    # Python's \w alone does not include all of these characters.
    token_char = r"[\w\u0D00-\u0D7F\u200C\u200D]"

    for source, target in NORMALIZATION_RULES.items():
        normalized = re.sub(
            rf"(?<!{token_char}){re.escape(source)}(?!{token_char})",
            target,
            normalized,
        )

    return normalized


def normalize_roman_malayalam(text: str) -> str:
    """
    Apply the Phase 7 Experiment 2 Roman Malayalam normalization candidate.

    Rules are applied only to complete Roman tokens. The candidate was
    selected using the separate Phase 7 development dataset.
    """
    if not text or not text.strip():
        return ""

    normalized = text.strip()

    for source, target in ROMAN_NORMALIZATION_RULES.items():
        normalized = re.sub(
            rf"(?<!\w){re.escape(source)}(?!\w)",
            target,
            normalized,
        )

    return normalized
