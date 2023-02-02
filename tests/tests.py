import pytest
import requests
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
import json

from socketio import AsyncClient
from app import app

import base64

@pytest.fixture
def api_client():
    return TestClient(app)

# user tests
# --------------------------------------------
def test_create_user(api_client):
    photo = open("tests/test.jpg", "rb")
    base64_photo = base64.b64encode(photo.read()).decode("utf-8")
    data = {"phone": "123456789", \
            "photo": base64_photo,
            "password": "password123"}
    data = json.dumps(data)
    response = api_client.post("/user/create", content=data)
    print(response.json())
    # code may be 403 or 201
    if response.status_code == 201:
        assert response.status_code == 201
    else:
        assert response.status_code == 403
        assert response.json()["detail"] == "User with this phone already exists"


def test_get_user_me(api_client):
    login_data = {"username": "123456789", "password": "password123"}
    login_response = api_client.post("/user/login", data=login_data)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response = api_client.get("/user/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["phone"] == login_data["username"]

def test_get_user_by_id(api_client):
    login_data = {"username": "123456789", "password": "password123"}
    login_response = api_client.post("/user/login", data=login_data)
    assert login_response.status_code == 200


    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    me = api_client.get("/user/me", headers=headers)
    assert me.status_code == 200
    me = me.json()
    
    response = api_client.get(f"/user/{me['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["phone"] == login_data["username"]


def test_login(api_client):
    login_data = {"username": "123456789", "password": "password123"}
    login_response = api_client.post("/user/login", data=login_data)
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

# chat tests
# --------------------------------------------
# don't know how to test socketio :(
def test_get_chat_list(api_client):
    access_token = get_access_token(api_client)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = api_client.get("/chat/", headers=headers)
    assert response.status_code == 200

def test_get_chat_by_id(api_client):
    access_token = get_access_token(api_client)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = api_client.get("/chat/111111", headers=headers)
    assert response.status_code == 404

def test_get_pinned_chats(api_client):
    access_token = get_access_token(api_client)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = api_client.get("/chat/pinned", headers=headers)
    assert response.status_code == 200

# message tests
# --------------------------------------------
def test_get_messages(api_client):
    access_token = get_access_token(api_client)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = api_client.get("/message/111111", headers=headers)
    assert response.status_code == 404

# helpers
# --------------------------------------------
def get_access_token(api_client):
    login_data = {"username": "123456789", "password": "password123"}
    login_response = api_client.post("/user/login", data=login_data)
    return login_response.json()["access_token"]

# for run tests:
# pytest python -m pytest tests/tests.py


