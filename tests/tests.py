import pytest
import requests
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse

from app import app

import base64

@pytest.fixture
def api_client():
    return TestClient(app)


def test_create_user(api_client):
    photo = open("tests/test.jpg", "rb")
    base64 = base64.b64encode(photo.read())
    data = {"phone": "123456789", "photo:": base64, "password": "password123"}
    response = api_client.post("/user/create", data=data)
    assert response.status_code == 201


def test_get_user_me(api_client):
    data = {"phone": "123456789", "password": "password123"}
    login_response = api_client.post("/user/login", data=data)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response = api_client.get("/user/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["phone"] == data["phone"]


# def test_get_user_by_id(api_client):
#     data = {"email": "test@example.com", "password": "password123"}
#     login_response = api_client.post("/user/login", data=data)
#     assert login_response.status_code == 200

#     access_token = login_response.json()["access_token"]
#     headers = {"Authorization": f"Bearer {access_token}"}

#     response = api_client.get("/user/1", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["email"] == data["email"]


# def test_login(api_client):
#     data = {"email": "test@example.com", "password": "password123"}
#     response = api_client.post("/user/login", data=data)
#     assert response.status_code == 200
#     assert "access_token" in response.json()
