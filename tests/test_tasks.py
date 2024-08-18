from app.main import app  # добавляем наше приложение
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def client():
    return TestClient(app)


def test_tasks(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    #  assert response.json() == [{}]
