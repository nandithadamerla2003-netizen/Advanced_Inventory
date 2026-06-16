from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_inventory():

    response = client.get("/inventory")

    assert response.status_code == 200