from fastapi.testclient import TestClient

from backend.app import main as api
from backend.app.lid import IndicLID, IndicLIDUnavailableError

client = TestClient(api.app)


class FakeLIDEngine:
    def __init__(self, code):
        self.code = code
        self.calls = []

    def batch_predict(self, texts, batch_size):
        self.calls.append((texts, batch_size))
        return [(texts[0], self.code, 0.9, "IndicLID-FTR")]


def fail_if_loaded():
    raise AssertionError("This model must not be loaded for this route.")


def test_adapter_returns_language_code_without_mislabeling_score():
    engine = FakeLIDEngine("mal_Latn")

    result = IndicLID(model=engine).predict("  veedu  ")

    assert result.code == "mal_Latn"
    assert result.confidence is None
    assert engine.calls == [(["veedu"], 1)]


def test_api_uses_indiclid_to_route_unmarked_roman_text(monkeypatch):
    engine = FakeLIDEngine("mal_Latn")
    calls = []

    class FakeXlit:
        def translit_sentence(self, text, lang_code):
            calls.append(("xlit", text, lang_code))
            return "വീട്"

    class FakeTranslator:
        def translate(self, text):
            calls.append(("translate", text))
            return "house"

    monkeypatch.setattr(api, "get_indiclid_engine", lambda: engine)
    monkeypatch.setattr(api, "get_indicxlit_engine", FakeXlit)
    monkeypatch.setattr(api, "get_indictrans2_engine", FakeTranslator)

    response = client.post("/translate", json={"text": "veedu"})

    assert response.status_code == 200
    assert response.json()["language"] == "roman_malayalam"
    assert response.json()["translation"] == "house"
    assert engine.calls == [(["veedu"], 1)]
    assert calls == [("xlit", "veedu", "ml"), ("translate", "വീട്")]


def test_api_uses_indiclid_english_prediction_over_marker_fallback(monkeypatch):
    engine = FakeLIDEngine("eng_Latn")

    monkeypatch.setattr(api, "get_indiclid_engine", lambda: engine)
    monkeypatch.setattr(api, "get_indicxlit_engine", fail_if_loaded)
    monkeypatch.setattr(api, "get_indictrans2_engine", fail_if_loaded)

    response = client.post(
        "/translate",
        json={"text": "njan innu busy aanu"},
    )

    assert response.status_code == 200
    assert response.json()["language"] == "english"
    assert response.json()["translation"] == "njan innu busy aanu"
    assert engine.calls == [(["njan innu busy aanu"], 1)]


def test_api_returns_503_if_configured_indiclid_fails(monkeypatch):
    def fail_lid():
        raise IndicLIDUnavailableError("IndicLID initialization failed.")

    monkeypatch.setattr(api, "get_indiclid_engine", fail_lid)
    monkeypatch.setattr(api, "get_indicxlit_engine", fail_if_loaded)
    monkeypatch.setattr(api, "get_indictrans2_engine", fail_if_loaded)

    response = client.post("/translate", json={"text": "hello"})

    assert response.status_code == 503
    assert response.json()["detail"] == "IndicLID initialization failed."
