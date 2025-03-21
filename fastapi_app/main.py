from fastapi import FastAPI
from fastapi_app.routers import tasks
from fastapi_app.dependencies import init_db

app = FastAPI()

# Инициализация базы данных
init_db()

# Подключаем роутер
app.include_router(tasks.router)

# Пример корневого эндпоинта
@app.get("/")
def read_root():
    return {"message": "Task Manager API is running"}
