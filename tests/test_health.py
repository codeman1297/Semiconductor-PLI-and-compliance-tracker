"""Phase 1 smoke tests: the app boots, the database answers, the templates render."""

from fastapi.testclient import TestClient


def test_healthz(client: TestClient) -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz_touches_the_database(client: TestClient) -> None:
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["database"] == "ok"


def test_home_renders_with_the_disclaimer(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Not legal, financial, or tax advice" in response.text
