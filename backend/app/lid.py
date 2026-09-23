"""Backend adapter for AI4Bharat IndicLID."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LIDResult:
    code: str
    confidence: float | None = None


class IndicLIDUnavailableError(RuntimeError):
    """Raised when the IndicLID runtime is not configured or fails."""


class IndicLID:
    def __init__(self, model: Any | None = None) -> None:
        self._model = model

    def predict(self, text: str) -> LIDResult:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        if self._model is None:
            raise IndicLIDUnavailableError(
                "IndicLID model/runtime is not configured in this environment."
            )

        predictions = self._model.batch_predict([text.strip()], batch_size=1)

        if len(predictions) != 1 or len(predictions[0]) != 4:
            raise IndicLIDUnavailableError(
                "IndicLID returned an unexpected prediction format."
            )

        _, code, _score, _model_name = predictions[0]

        if not isinstance(code, str) or not code:
            raise IndicLIDUnavailableError(
                "IndicLID returned an invalid language code."
            )

        # FastText scores and BERT logits are not interchangeable
        # confidence probabilities.
        return LIDResult(code=code)
