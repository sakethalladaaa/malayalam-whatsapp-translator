"""
Phase 9 — Backend-facing IndicXlit adapter.

This module keeps the production pipeline independent from the concrete
IndicXlit runtime and allows tests to inject a lightweight fake engine.
"""

from __future__ import annotations

from typing import Any


class IndicXlitUnavailableError(RuntimeError):
    """Raised when IndicXlit inference is requested without a runtime."""


class IndicXlit:
    """Backend adapter for Roman Malayalam transliteration."""

    def __init__(self, engine: Any | None = None) -> None:
        self._engine = engine

    def transliterate(self, text: str) -> str:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        if self._engine is None:
            raise IndicXlitUnavailableError(
                "IndicXlit model/runtime is not configured in this environment."
            )

        return self._engine.translit_sentence(
            text.strip(),
            lang_code="ml",
        )
