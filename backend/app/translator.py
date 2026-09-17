"""
Phase 9 — Backend-facing IndicTrans2 adapter.

This module isolates the translation pipeline from the concrete
IndicTrans2 runtime and allows tests to inject a lightweight fake engine.
"""

from __future__ import annotations

from typing import Any


class IndicTrans2UnavailableError(RuntimeError):
    """Raised when IndicTrans2 inference is requested without a runtime."""


class IndicTrans2:
    """Backend adapter for Malayalam-to-English translation."""

    def __init__(self, engine: Any | None = None) -> None:
        self._engine = engine

    def translate(self, text: str) -> str:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        if self._engine is None:
            raise IndicTrans2UnavailableError(
                "IndicTrans2 model/runtime is not configured in this environment."
            )

        return self._engine.translate(text.strip())
