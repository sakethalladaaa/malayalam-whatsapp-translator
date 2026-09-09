from ai4bharat.transliteration import XlitEngine


def create_engine() -> XlitEngine:
    return XlitEngine(
        src_script_type="roman",
        beam_width=10,
        rescore=False,
    )


def transliterate(text: str, engine=None) -> str:
    if not text or not text.strip():
        return ""

    if engine is None:
        engine = create_engine()

    return engine.translit_sentence(
        text.strip(),
        lang_code="ml",
    )
