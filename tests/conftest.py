import pytest
from fastapi.testclient import TestClient

from fastapi_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def creat_user(client):
    response = client.post(
        '/users/1',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': '456123',
        },
    )
    return response
