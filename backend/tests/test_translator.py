import pytest

from backend.app.translator import (
    IndicTrans2,
    IndicTrans2UnavailableError,
)


class FakeIndicTrans2Engine:
    def translate(self, text):
        return f"EN:{text}"


def test_translate_malayalam_to_english():
    translator = IndicTrans2(engine=FakeIndicTrans2Engine())

    result = translator.translate("നാളെ വരാം")

    assert result == "EN:നാളെ വരാം"


def test_translate_strips_input():
    translator = IndicTrans2(engine=FakeIndicTrans2Engine())

    result = translator.translate("  നാളെ വരാം  ")

    assert result == "EN:നാളെ വരാം"


def test_empty_input_is_rejected():
    translator = IndicTrans2(engine=FakeIndicTrans2Engine())

    with pytest.raises(ValueError, match="Text cannot be empty"):
        translator.translate("   ")


def test_unavailable_runtime_is_explicit():
    translator = IndicTrans2()

    with pytest.raises(IndicTrans2UnavailableError):
        translator.translate("നാളെ വരാം")
