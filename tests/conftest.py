from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import pytest

TEST_DATABASE_URL = "sqlite:///./test.db"  # Тестовая база данных

engine_test = create_engine(TEST_DATABASE_URL, connect_args={
                                   "check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine_test)
Base = declarative_base()
