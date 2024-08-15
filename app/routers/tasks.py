from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..database import SessionLocal, engine
"""
Диспечер запросов tasks
"""
models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, user_id: int,
                db: Session = Depends(get_db)):
    """Метод создает задачу для одного пользователя"""
    return crud.create_task(db=db, task=task, user_id=user_id)


@router.get("/tasks/", response_model=List[schemas.Task])
def tasks_list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Метод выводит список задач через фильтр по статусу"""
    tasks = crud.tasks_list(db, skip=skip, limit=limit)
    return tasks


@router.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """Метод выводит задачу по task_id"""
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate,
                db: Session = Depends(get_db)):
    """Метод получает новые название и описание 
    для одной задачи и записывает их в бд"""
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db_task.description = task.description
    db_task.completed = task.completed
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Метод удаляет указанную задачу"""
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return db_task
