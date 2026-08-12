from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.base import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Этот код сработает строго при старте бэкенда
    init_db()  # Автоматически создаем таблицы в БД SQLite
    yield

# Создаем приложение и подключаем жизненный цикл (lifespan)
app = FastAPI(title="Movie DB API", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "Бэкенд запущен, таблицы в БД созданы!"}
