from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_running_message() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Restaurant QR Ordering API is running"}


def test_health_endpoint_returns_healthy_status() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "restaurant-qr-ordering-api",
    }
