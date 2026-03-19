# 2026.03.19 19:05 IMM (ОБНОВЛЕНО: работа с БД)

# ГЛАВНЫЙ ВХОД, ОБЩИЕ ЭНДПОИНТЫ

from typing import Any, Dict

from sqlalchemy.orm import Session

from app.api.parts import router as parts_router
from app.db.database import get_db  # функция для получения сессии
from app.db.models import PartDB  # модель таблицы parts
from fastapi import Depends, FastAPI

# 1. СОЗДАНИЕ ПРИЛОЖЕНИЯ FASTAPI
app = FastAPI(title="Garage API", description="API для учета запчастей в гараже")

# 2. ПОДКЛЮЧЕНИЕ РОУТЕРА С ЭНДПОИНТАМИ ДЛЯ ЗАПЧАСТЕЙ
app.include_router(parts_router)


# 3. КОРНЕВОЙ ЭНДПОИНТ (GET /)
@app.get("/")
def read_root() -> Dict[str, Any]:
    """Основная страница API с информацией о доступных эндпоинтах"""
    return {
        "message": "Garage API работает!",
        "endpoints": {
            "parts_list": "/parts",
            "health_check": "/health",
            "docs": "/docs",
        },
    }


# 4. ЭНДПОИНТ ПРОВЕРКИ ЗДОРОВЬЯ (GET /health)
# Теперь получаем количество запчастей напрямую из базы данных
@app.get("/health")
def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Проверка состояния сервиса (используется системами мониторинга)"""
    total_parts = db.query(PartDB).count()  # считаем записи в таблице parts
    return {
        "status": "OK",
        "total_parts": total_parts,
        "service": "garage-api",
        "version": "0.1.0",
    }


# 5. ЗАПУСК СЕРВЕРА (при прямом запуске файла)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
