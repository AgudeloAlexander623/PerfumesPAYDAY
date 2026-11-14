from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "security-service"}
    assert response.headers["x-request-id"]


def test_request_id_is_propagated(client: TestClient) -> None:
    response = client.get("/health", headers={"x-request-id": "req-de-prueba"})

    assert response.headers["x-request-id"] == "req-de-prueba"


def test_not_found_uses_error_envelope(client: TestClient) -> None:
    response = client.get("/ruta-inexistente")

    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "NOT_FOUND"
    assert body["error"]["requestId"] == response.headers["x-request-id"]