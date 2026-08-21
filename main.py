from fastapi import FastAPI
from tasks.routers import router as tasks_router
from users.router import router as users_router
from tasks import models
from users import models

app = FastAPI(title="todo app api", description="this is an example desciption", version="1.0.0")

app.include_router(tasks_router)
app.include_router(users_router)