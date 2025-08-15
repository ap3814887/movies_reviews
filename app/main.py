import os
import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from .database import Base, engine

app = FastAPI(title="Movie Reviews API")


def run_migrations():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(["alembic", "upgrade", "head"], check=True, cwd=project_root)


@app.on_event("startup")
def startup_event():
    run_migrations()


# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем маршруты
app.include_router(router)
