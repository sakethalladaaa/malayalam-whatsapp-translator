"""
Phase 9 — Translation pipeline orchestration.

Connects the existing language router with Phase 7 preprocessing,
IndicXlit transliteration, and IndicTrans2 translation adapters.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.app.router import route_language
from phase7.preprocessing import (
    normalize_malayalam,
    normalize_roman_malayalam,
)


class MixedTextUnsupportedError(RuntimeError):
    """Raised until mixed Malayalam-English processing is implemented."""


@dataclass(frozen=True)
class PipelineResult:
    route: str
    translation: str


class TranslationPipeline:
    def __init__(
        self,
        transliterator: Any,
        translator: Any,
    ) -> None:
        self._transliterator = transliterator
        self._translator = translator

    def process(
        self,
        text: str,
        indiclid_code: str | None = None,
    ) -> PipelineResult:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        cleaned_text = text.strip()
        route = route_language(cleaned_text, indiclid_code)

        if route == "english":
            return PipelineResult(
                route=route,
                translation=cleaned_text,
            )

        if route == "malayalam_native":
            return PipelineResult(
                route=route,
                translation=self._translator.translate(cleaned_text),
            )

        if route == "roman_malayalam":
            normalized_roman = normalize_roman_malayalam(cleaned_text)

            malayalam_text = self._transliterator.transliterate(
                normalized_roman
            )

            normalized_malayalam = normalize_malayalam(
                malayalam_text
            )

            return PipelineResult(
                route=route,
                translation=self._translator.translate(
                    normalized_malayalam
                ),
            )

        if route == "mixed":
            raise MixedTextUnsupportedError(
                "Mixed Malayalam-English processing is not implemented yet."
            )

        raise RuntimeError(f"Unsupported route: {route}")
