import os
import sys

# Add Backend directory to Python path
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

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