from app.main import app  # добавляем наше приложение
from .conftest import TestingSessionLocal, init_db
from fastapi.testclient import TestClient
import pytest

"""
Описание тестов:

- test_create_task: Создание тестовой задачи.
- test_read_task: Проверяет возможность чтения информации о задаче.
- test_update_task: Проверяет возможность обновления информации задачи.
- test_delete_task: Проверяет возможность удаления задачи
     и подтверждает, что задача удалена.
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


task_data = {"title": "TEST TASK", 
             "description": "delete me", 
             "completed": "false"}


@pytest.fixture
def create_task(client, db_session):
    response = client.post("/tasks/", json=task_data)
    return response.json()


def test_create_task(client, db_session):
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    assert response.json()["title"] == "TEST TASK"
   

def test_read_task(client, db_session):
    response = client.get("/tasks/1")
    assert response.status_code == 200
    # assert response.json() == create_user


def test_update_task(client, db_session):
    response = client.put("/tasks/1", json={"title": "TEST TASK", 
                                            "description": "delete me", 
                                            "completed": "True"})
    assert response.status_code == 200
    assert response.json()["completed"] == "true"


def test_delete_task(client, db_session):
    response = client.delete("/tasks/1")
    assert response.status_code == 200

    response = client.get("/tasks/1")  # проверка что user удалился
    assert response.status_code == 404
