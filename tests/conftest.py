from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base


# Создание тестовой базы данных
TEST_DATABASE_URL = "sqlite:///./test.db"

engine_test = create_engine(TEST_DATABASE_URL, 
                            connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, 
                                   autoflush=False, 
                                   bind=engine_test)


def init_db():
    Base.metadata.create_all(bind=engine_test)
