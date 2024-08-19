from app.main import app  # добавляем наше приложение
from conftest import TestingSessionLocal  # добавляем тестовую бд
from fastapi.testclient import TestClient
import pytest
import app.crud as crud

#Base.metadata.drop_all(bind=engine)  # Удаляем таблицы после тестов
#Base.metadata.create_all(bind=engine)  # Восстанавливаем таблицы


def get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():  # Новый клиент
    def _get_test_db_override():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = _get_test_db_override
    return TestClient(app)


def test_tasks(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    #  assert response.json() == [{}]


def test_create_task(client):  # TODO как обратиться -> crud.create_task(db = ...)
    """Метод создает задачу для одного пользователя"""
    client.post("/tasks/", json={"name": "Test Item"})
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    # assert crud.create_task()
