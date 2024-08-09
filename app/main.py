from fastapi import FastAPI
from .routers import users, tasks

app = FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)

# uvicorn example:app --log-config /path/to/log.ini
