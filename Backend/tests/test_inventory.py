from fastapi.testclient import TestClient

from main import app
from config import ADMIN_USERNAME, ADMIN_PASSWORD

client = TestClient(app)


def get_access_token():

    response = client.post(
        "/auth/login",
        data={
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_inventory():

    token = get_access_token()

    response = client.get(
        "/inventory/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_dashboard():

    token = get_access_token()

    response = client.get(
        "/inventory/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200