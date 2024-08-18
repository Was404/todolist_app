from app.main import app  # добавляем наше приложение
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def client():
    return TestClient(app)


def test_get_user(client):
    response = client.get("/users/")
    assert response.status_code == 200
    #  assert response.json() == [{}]
