"""
Phase 8 — Malayalam-family routing.

Phase 5 established the routing policy and froze candidate_v1, but the
original lexical-marker implementation was not committed to the repository.
This module therefore implements a conservative Phase 8 reconstruction of
that documented policy; it is not claimed to be the original candidate_v1
source implementation.
"""

from __future__ import annotations

import re
from typing import Final

SHORT_TEXT_MAX_WORDS: Final[int] = 4
SHORT_TEXT_REQUIRED_MARKERS: Final[int] = 1
LONG_TEXT_REQUIRED_MARKERS: Final[int] = 2


# Conservative Phase 8 marker inventory.
# This is an implementation choice, not recovered Phase 5 source code.
ROMAN_MALAYALAM_MARKERS: Final[frozenset[str]] = frozenset(
    {
        "njan",
        "enikku",
        "ninakku",
        "nee",
        "innu",
        "ippo",
        "nale",
        "evide",
        "entha",
        "undo",
        "aano",
        "aayo",
        "kazhicho",
        "varunundo",
        "paripadi",
        "chetta",
        "shari",
        "alle",
        "aan",
        "vilikkam",
        "varam",
        "cheytho",
        "pokunnu",
    }
)


def _normalize_words(text: str) -> list[str]:
    return re.findall(r"[\w]+(?:['-][\w]+)*", text.lower())


def roman_malayalam_fallback(text: str) -> bool:
    """
    Apply the documented Phase 5 fallback thresholds using the
    Phase 8 conservative marker inventory.
    """
    words = _normalize_words(text)

    if not words:
        return False

    marker_hits = sum(word in ROMAN_MALAYALAM_MARKERS for word in words)

    required_hits = (
        SHORT_TEXT_REQUIRED_MARKERS
        if len(words) <= SHORT_TEXT_MAX_WORDS
        else LONG_TEXT_REQUIRED_MARKERS
    )

    return marker_hits >= required_hits


def contains_malayalam_script(text: str) -> bool:
    """Return True when text contains Malayalam Unicode characters."""
    return any("\u0d00" <= char <= "\u0d7f" for char in text)


def route_language(
    text: str,
    indiclid_code: str | None = None,
) -> str:
    """
    Route text into one of four backend processing categories:

    - malayalam_native
    - roman_malayalam
    - mixed
    - english
    """
    text = text.strip()
    code = (indiclid_code or "").strip()

    if code == "mal_Mlym":
        return "malayalam_native"

    if code == "mal_Latn":
        return "roman_malayalam"

    if contains_malayalam_script(text):
        return (
            "mixed"
            if any(char.isascii() and char.isalpha() for char in text)
            else "malayalam_native"
        )

    if code == "eng_Latn":
        return "english"

    if roman_malayalam_fallback(text):
        return "roman_malayalam"

    return "english"
