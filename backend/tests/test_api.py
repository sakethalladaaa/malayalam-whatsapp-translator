import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_translate_scaffold_trims_input(client):
    response = client.post("/translate", json={"text": "  നമസ്കാരം  "})
    assert response.status_code == 200
    assert response.json() == {
        "input": "നമസ്കാരം",
        "language": "unknown",
        "translation": None,
    }


@pytest.mark.parametrize("payload", [
    {},
    {"text": ""},
    {"text": "   "},
    {"text": "\t\n"},
    {"text": None},
    {"text": 123},
    {"text": ["hello"]},
    {"text": "a" * 5001},
])
def test_translate_rejects_invalid_input(client, payload):
    response = client.post("/translate", json=payload)
    assert response.status_code == 422
    assert any(
        error["loc"] == ["body", "text"]
        for error in response.json()["detail"]
    )


def test_translate_accepts_maximum_length(client):
    text = "a" * 5000
    response = client.post("/translate", json={"text": text})
    assert response.status_code == 200
    assert response.json()["input"] == text
