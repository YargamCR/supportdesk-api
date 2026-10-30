from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "name": "SupportDesk API",
        "status": "running",
        "version": "0.1.0",
    }
