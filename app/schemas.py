from pydantic import BaseModel
from typing import List, Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    owner_id: int
    # completed: bool
    # created_at: str  # когда была создана задача

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str  # нужна валидация данных Field(@mail\@bk\@gmail...) TODO
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    tasks: List[Task] = []

    class Config:
        orm_mode = True


# created_at: Optional[str]

