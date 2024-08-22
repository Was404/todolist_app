from app.main import app  # добавляем наше приложение
from .conftest import TestingSessionLocal, init_db
from fastapi.testclient import TestClient
import pytest

"""
Описание тестов:

- test_create_user: Создание тестового пользователя.
- test_users_list: Проверяет возможность чтения списка пользователей
- test_read_user: Проверяет возможность чтения информации о пользователе.
- test_update_user: Проверяет возможность обновления информации о пользователе.
- test_delete_user: Проверяет возможность удаления пользователя
     и подтверждает, что он был удалён.
"""


@pytest.fixture(scope="module")
def client():
    # Инициализация тестовой базы данных
    init_db()
    # Создание клиентского объекта
    client = TestClient(app)
    yield client

    # добавить очистку базы данных TODO


@pytest.fixture(scope="module")
def db_session():
    # Настройка сессии для тестов
    connection = TestingSessionLocal()
    yield connection
    connection.close()


user_data = {"username": "TestUser", 
             "email": "test@gmail", 
             "full_name": "Tester Testerson", 
             "password": "123test"}


@pytest.fixture
def create_user(client, db_session):
    response = client.post("/users/", json=user_data)
    return response.json()


def test_create_user(client, db_session):
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "TestUser"


def test_users_list(client, db_session):
    response = client.get("users/?skip=0&limit=10")
    assert response.status_code == 200
    assert response.json()
  

def test_read_user(client, db_session):
    response = client.get("/users/1")
    assert response.status_code == 200
    # assert response.json() == create_user


def test_update_user(client, db_session):
    response = client.put("/users/1", json={"username": "string", 
                                            "email": "string", 
                                            "full_name": "string", 
                                            "password": "string"})
    assert response.status_code == 200
    assert response.json()["username"] == "string"


def test_delete_user(client, db_session):
    response = client.delete("/users/1")
    assert response.status_code == 200

    response = client.get("/users/1")  # проверка что user удалился
    assert response.status_code == 404
