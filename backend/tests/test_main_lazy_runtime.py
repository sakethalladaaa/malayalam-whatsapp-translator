from fastapi.testclient import TestClient

from backend.app import main as api

client = TestClient(api.app)


def fail_if_loaded():
    raise AssertionError("This model must not be loaded for this route.")


def test_english_does_not_load_models(monkeypatch):
    monkeypatch.setattr(api, "get_indicxlit_engine", fail_if_loaded)
    monkeypatch.setattr(api, "get_indictrans2_engine", fail_if_loaded)

    response = client.post(
        "/translate",
        json={"text": "Can you send me the file?"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "input": "Can you send me the file?",
        "language": "english",
        "translation": "Can you send me the file?",
    }


def test_native_malayalam_only_loads_indictrans2(monkeypatch):
    calls = []

    class FakeTranslatorEngine:
        def translate(self, text):
            calls.append(("translate", text))
            return "I will come tomorrow."

    def load_translator():
        calls.append(("load", "indictrans2"))
        return FakeTranslatorEngine()

    monkeypatch.setattr(api, "get_indicxlit_engine", fail_if_loaded)
    monkeypatch.setattr(api, "get_indictrans2_engine", load_translator)

    response = client.post(
        "/translate",
        json={"text": "നാളെ ഞാൻ വരും."},
    )

    assert response.status_code == 200
    assert response.json()["language"] == "malayalam_native"
    assert response.json()["translation"] == "I will come tomorrow."
    assert calls == [
        ("load", "indictrans2"),
        ("translate", "നാളെ ഞാൻ വരും."),
    ]


def test_roman_malayalam_loads_both_models(monkeypatch):
    calls = []

    class FakeXlitEngine:
        def translit_sentence(self, text, lang_code):
            calls.append(("transliterate", text, lang_code))
            return "നാളെ വരാം"

    class FakeTranslatorEngine:
        def translate(self, text):
            calls.append(("translate", text))
            return "I will come tomorrow."

    def load_xlit():
        calls.append(("load", "indicxlit"))
        return FakeXlitEngine()

    def load_translator():
        calls.append(("load", "indictrans2"))
        return FakeTranslatorEngine()

    monkeypatch.setattr(api, "get_indicxlit_engine", load_xlit)
    monkeypatch.setattr(api, "get_indictrans2_engine", load_translator)

    response = client.post(
        "/translate",
        json={"text": "njan nale varam"},
    )

    assert response.status_code == 200
    assert response.json()["language"] == "roman_malayalam"
    assert response.json()["translation"] == "I will come tomorrow."
    assert calls == [
        ("load", "indicxlit"),
        ("transliterate", "njan naale varam", "ml"),
        ("load", "indictrans2"),
        ("translate", "നാളെ വരാം"),
    ]
