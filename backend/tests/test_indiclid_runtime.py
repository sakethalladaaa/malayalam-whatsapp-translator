import pytest
from fastapi.testclient import TestClient

from backend.app import indiclid_runtime
from backend.app import main as api
from backend.app.lid import IndicLIDUnavailableError


def test_unconfigured_runtime_returns_none(monkeypatch):
    monkeypatch.delenv("INDICLID_INFERENCE_DIR", raising=False)

    assert indiclid_runtime.get_indiclid_engine() is None


def test_missing_model_files_raise_explicit_error(monkeypatch, tmp_path):
    monkeypatch.setenv("INDICLID_INFERENCE_DIR", str(tmp_path))

    with pytest.raises(
        IndicLIDUnavailableError,
        match="failed to initialize",
    ):
        indiclid_runtime.get_indiclid_engine()


def test_api_returns_503_when_configured_models_are_missing(monkeypatch, tmp_path):
    monkeypatch.setenv("INDICLID_INFERENCE_DIR", str(tmp_path))

    response = TestClient(api.app).post(
        "/translate",
        json={"text": "Hello"},
    )

    assert response.status_code == 503
    assert "IndicLID" in response.json()["detail"]
