import pytest

from backend.app.transliterator import IndicXlit
from phase7.preprocessing import normalize_roman_malayalam

pytestmark = pytest.mark.indicxlit_runtime


def has_malayalam_script(text: str) -> bool:
    return any("\u0D00" <= char <= "\u0D7F" for char in text)


def test_real_indicxlit_runtime_initializes(real_indicxlit_engine):
    assert real_indicxlit_engine is not None
    assert callable(real_indicxlit_engine.translit_sentence)


def test_real_runtime_transliterates_roman_malayalam(real_indicxlit_engine):
    output = real_indicxlit_engine.translit_sentence(
        "vegam vaa",
        lang_code="ml",
    )

    assert isinstance(output, str)
    assert output.strip()
    assert has_malayalam_script(output)


@pytest.mark.parametrize(
    "text",
    [
        "ninakku innu sukhamano?",
        "njan innu college-il pokunnu",
        "evideya?",
        "shari chetta",
        "vegam vaa",
        "nale class undo?",
    ],
)
def test_real_runtime_handles_whatsapp_style_inputs(
    real_indicxlit_engine,
    text,
):
    output = real_indicxlit_engine.translit_sentence(
        text,
        lang_code="ml",
    )

    assert isinstance(output, str)
    assert output.strip()
    assert has_malayalam_script(output)


def test_roman_normalization_flows_into_real_indicxlit(
    real_indicxlit_engine,
):
    normalized = normalize_roman_malayalam("njan nale varam")

    assert normalized == "njan naale varam"

    output = real_indicxlit_engine.translit_sentence(
        normalized,
        lang_code="ml",
    )

    assert isinstance(output, str)
    assert output.strip()
    assert has_malayalam_script(output)


def test_backend_adapter_uses_real_indicxlit_engine(
    real_indicxlit_engine,
):
    transliterator = IndicXlit(engine=real_indicxlit_engine)

    output = transliterator.transliterate("vegam vaa")

    assert isinstance(output, str)
    assert output.strip()
    assert has_malayalam_script(output)


def test_reused_engine_handles_multiple_inputs(real_indicxlit_engine):
    inputs = [
        "vegam vaa",
        "evideya?",
        "nale class undo?",
    ]

    outputs = [
        real_indicxlit_engine.translit_sentence(text, lang_code="ml")
        for text in inputs
    ]

    assert len(outputs) == 3
    assert all(isinstance(output, str) for output in outputs)
    assert all(output.strip() for output in outputs)
    assert all(has_malayalam_script(output) for output in outputs)


def test_same_input_is_stable_with_reused_engine(real_indicxlit_engine):
    output1 = real_indicxlit_engine.translit_sentence(
        "vegam vaa",
        lang_code="ml",
    )
    output2 = real_indicxlit_engine.translit_sentence(
        "vegam vaa",
        lang_code="ml",
    )

    assert output1 == output2


def test_indicxlit_engine_is_loaded_once(real_indicxlit_engine):
    from backend.app.indicxlit_runtime import get_indicxlit_engine

    engine1 = get_indicxlit_engine()
    engine2 = get_indicxlit_engine()

    assert engine1 is real_indicxlit_engine
    assert engine2 is engine1
    assert get_indicxlit_engine.cache_info().misses == 1


def test_cached_runtime_does_not_require_model_redownload(
    real_indicxlit_engine,
    monkeypatch,
):
    import os

    from ai4bharat.transliteration.transformer import base_engine, en2indic

    from backend.app.indicxlit_runtime import get_indicxlit_engine

    if en2indic.is_directory_writable(en2indic.F_DIR):
        models_root = os.path.join(en2indic.F_DIR, "models")
    else:
        models_root = os.path.expanduser("~/.AI4Bharat_Xlit_Models")

    model_path = os.path.join(
        models_root,
        "en2indic",
        en2indic.XLIT_VERSION,
        base_engine.MODEL_FILE,
    )

    assert os.path.isfile(model_path), (
        f"Expected cached IndicXlit model at {model_path}"
    )

    def fail_if_downloaded(*args, **kwargs):
        raise AssertionError(
            "Cached IndicXlit initialization attempted a model download."
        )

    monkeypatch.setattr(base_engine, "dload", fail_if_downloaded)

    get_indicxlit_engine.cache_clear()
    engine = get_indicxlit_engine()

    assert engine is not None
    assert callable(engine.translit_sentence)
