from fastapi import FastAPI
from .routers import users, tasks

app = FastAPI(
    tittle="ToDo List App"
)

app.include_router(users.router, tags=["Users"])
app.include_router(tasks.router, tags=["Tasks"])

# uvicorn app.main:app --log-config env/log.ini
