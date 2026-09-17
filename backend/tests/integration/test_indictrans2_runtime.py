from __future__ import annotations

import os

import pytest

from backend.app.indictrans2_runtime import get_indictrans2_engine
from backend.app.translator import IndicTrans2

RUN_REAL_RUNTIME = os.getenv("RUN_INDICTRANS2_INTEGRATION") == "1"

pytestmark = [
    pytest.mark.indictrans2_runtime,
    pytest.mark.skipif(
        not RUN_REAL_RUNTIME,
        reason="Set RUN_INDICTRANS2_INTEGRATION=1 to run real IndicTrans2 tests.",
    ),
]


@pytest.fixture(scope="session")
def real_indictrans2_engine():
    return get_indictrans2_engine()


def test_real_runtime_initializes(real_indictrans2_engine):
    assert real_indictrans2_engine is not None
    assert real_indictrans2_engine.device in {"mps", "cpu"}


def test_real_malayalam_to_english_translation(real_indictrans2_engine):
    translator = IndicTrans2(engine=real_indictrans2_engine)

    result = translator.translate("നാളെ ഞാൻ വീട്ടിലേക്ക് വരും.")

    assert isinstance(result, str)
    assert result.strip()
    assert result != "നാളെ ഞാൻ വീട്ടിലേക്ക് വരും."


def test_runtime_engine_is_reused():
    first = get_indictrans2_engine()
    second = get_indictrans2_engine()

    assert first is second


@pytest.mark.parametrize(
    "text",
    [
        "എനിക്ക് സുഖമാണ്.",
        "നാളെ കാണാം.",
        "ഞാൻ വീട്ടിലേക്കു പോകുന്നു.",
    ],
)
def test_representative_malayalam_inputs_translate(
    real_indictrans2_engine,
    text,
):
    translator = IndicTrans2(engine=real_indictrans2_engine)

    result = translator.translate(text)

    assert isinstance(result, str)
    assert result.strip()
    assert result != text
