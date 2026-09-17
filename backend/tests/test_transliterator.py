import pytest

from backend.app.transliterator import (
    IndicXlit,
    IndicXlitUnavailableError,
)


class FakeIndicXlitEngine:
    def translit_sentence(self, text, lang_code):
        assert lang_code == "ml"
        return f"ML:{text}"


def test_transliterate_roman_malayalam():
    transliterator = IndicXlit(engine=FakeIndicXlitEngine())

    result = transliterator.transliterate("Njan innu varam")

    assert result == "ML:Njan innu varam"


def test_transliterate_strips_input():
    transliterator = IndicXlit(engine=FakeIndicXlitEngine())

    result = transliterator.transliterate("  Njan varam  ")

    assert result == "ML:Njan varam"


def test_empty_input_is_rejected():
    transliterator = IndicXlit(engine=FakeIndicXlitEngine())

    with pytest.raises(ValueError, match="Text cannot be empty"):
        transliterator.transliterate("   ")


def test_unavailable_runtime_is_explicit():
    transliterator = IndicXlit()

    with pytest.raises(IndicXlitUnavailableError):
        transliterator.transliterate("Njan innu varam")
