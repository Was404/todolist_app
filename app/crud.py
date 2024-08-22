from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models, schemas
"""
Здесь описаны методы работающие с базой данных  // Руководитель базой данных
"""


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(username=user.username, email=user.email,
                          full_name=user.full_name,
                          hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def tasks_list(db: Session, skip: int = 0, limit: int = 100):
    if skip < 0 or limit <= 0:
        raise ValueError("skip must be non-negative and limit must be positive")

    return (
        db.query(models.Task)
        .order_by(desc(models.Task.completed))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
