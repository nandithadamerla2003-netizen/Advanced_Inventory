from fastapi.testclient import TestClient

from main import app
from config import ADMIN_EMAIL, ADMIN_USERNAME, ADMIN_PASSWORD

client = TestClient(app)


def get_access_token():

    response = client.post(
        "/auth/login",
        data={
            "Email":ADMIN_EMAIL,
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_home():

    response = client.get("/")

    assert response.status_code == 200


def test_get_products():

    token = get_access_token()

    response = client.get(
        "/products/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)