from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_inventory():
    response = client.get("/inventory/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_dashboard():
    response = client.get("/inventory/dashboard")
    assert response.status_code == 200