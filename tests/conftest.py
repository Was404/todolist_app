from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from fastapi.testclient import TestClient
import pytest

# Создание тестовой базы данных
TEST_DATABASE_URL = "sqlite:///./test.db"

engine_test = create_engine(TEST_DATABASE_URL, 
                            connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, 
                                   autoflush=False, 
                                   bind=engine_test)


@pytest.fixture(scope="function", autouse=True)
def override_get_db():
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine_test)


@pytest.fixture  # Убери это TODO
def client():
    def _get_test_db_override():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = _get_test_db_override
    return TestClient(app)
