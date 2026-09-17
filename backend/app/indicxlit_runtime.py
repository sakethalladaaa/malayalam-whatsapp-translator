"""
Phase 9 — Production IndicXlit runtime loader.

The AI4Bharat IndicXlit stack is loaded lazily so normal backend imports do
not require the legacy model environment. Successful initialization is cached
so repeated backend use reuses one expensive model instance.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from backend.app.transliterator import IndicXlitUnavailableError


@lru_cache(maxsize=1)
def get_indicxlit_engine() -> Any:
    """
    Load and cache the validated AI4Bharat IndicXlit engine.

    The configuration matches the Phase 6 evaluation runtime.
    """
    os.environ.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")

    try:
        from ai4bharat.transliteration import XlitEngine
    except Exception as exc:
        raise IndicXlitUnavailableError(
            "IndicXlit runtime dependencies are not available."
        ) from exc

    try:
        return XlitEngine(
            src_script_type="roman",
            beam_width=10,
            rescore=False,
        )
    except Exception as exc:
        raise IndicXlitUnavailableError(
            "IndicXlit runtime/model failed to initialize."
        ) from exc
