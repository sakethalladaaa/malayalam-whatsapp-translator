import pytest

from backend.app.pipeline import (
    MixedTextUnsupportedError,
    TranslationPipeline,
)


class FakeTransliterator:
    def __init__(self):
        self.received = None

    def transliterate(self, text):
        self.received = text
        return "ഇന്നു വിളിക്കം"


class FakeTranslator:
    def __init__(self):
        self.received = None

    def translate(self, text):
        self.received = text
        return f"EN:{text}"


def test_english_is_returned_unchanged():
    pipeline = TranslationPipeline(
        transliterator=FakeTransliterator(),
        translator=FakeTranslator(),
    )

    result = pipeline.process(
        "Can you send me the file?",
        indiclid_code="eng_Latn",
    )

    assert result.route == "english"
    assert result.translation == "Can you send me the file?"


def test_native_malayalam_goes_directly_to_translation():
    translator = FakeTranslator()
    pipeline = TranslationPipeline(
        transliterator=FakeTransliterator(),
        translator=translator,
    )

    result = pipeline.process(
        "നാളെ വരാം",
        indiclid_code="mal_Mlym",
    )

    assert result.route == "malayalam_native"
    assert translator.received == "നാളെ വരാം"
    assert result.translation == "EN:നാളെ വരാം"


def test_roman_malayalam_uses_normalization_transliteration_and_translation():
    transliterator = FakeTransliterator()
    translator = FakeTranslator()
    pipeline = TranslationPipeline(
        transliterator=transliterator,
        translator=translator,
    )

    result = pipeline.process(
        "njan nale varam",
        indiclid_code="mal_Latn",
    )

    assert result.route == "roman_malayalam"
    assert transliterator.received == "njan naale varam"
    assert translator.received == "ഇന്ന് വിളിക്കാം"
    assert result.translation == "EN:ഇന്ന് വിളിക്കാം"


def test_mixed_text_is_explicitly_not_implemented_yet():
    pipeline = TranslationPipeline(
        transliterator=FakeTransliterator(),
        translator=FakeTranslator(),
    )

    with pytest.raises(MixedTextUnsupportedError):
        pipeline.process("നാളെ class online ആണോ?")
