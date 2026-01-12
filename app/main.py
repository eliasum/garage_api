# 2025.11.27 18:43 IMM

# Импорты
from typing import Any, Dict

from app.models import Garage  # бизнес-логика
from app.schemas.part import PartCreate, PartResponse  # Импортируем из папки schemas
from fastapi import APIRouter, FastAPI, HTTPException

# 1. СОЗДАНИЕ ПРИЛОЖЕНИЯ FASTAPI
# FastAPI() — конструктор, создаёт веб-приложение
# title, description — метаданные для документации

# FastAPI (реактивный, событийно-ориентированный)
# Что это: Приложение, которое ждет запросов и реагирует на них.
# Аналог из жизни: Работа курьерского сервиса. Ты ждешь заказов, и когда приходит заказ, выполняешь его.

# СОЗДАЕМ FASTAPI ПРИЛОЖЕНИЕ
app = FastAPI(title="Garage API", description="API для учета запчастей в гараже")

# 2. СОЗДАНИЕ ЭКЗЕМПЛЯРА GARAGE
# Это наше "хранилище данных" (пока в памяти)
garage = Garage()

# 3. ДОБАВЛЕНИЕ ТЕСТОВЫХ ДАННЫХ
# При каждом запуске сервера создаются 3 тестовые запчасти
garage.add_part("Масляный фильтр", "OC 90", 5)
garage.add_part("Воздушный фильтр", "AF 123", 3)
garage.add_part("Свеча зажигания", "SP 456", 10)

# 4. СОЗДАНИЕ РОУТЕРА ДЛЯ ЗАПЧАСТЕЙ
# APIRouter — группа эндпоинтов
# prefix="/parts" — все эндпоинты будут начинаться с /parts
# tags=["parts"] — группа в документации Swagger
router = APIRouter(prefix="/parts", tags=["parts"])


# 5. ЭНДПОИНТ СОЗДАНИЯ ЗАПЧАСТИ (POST)
# @router.post — декоратор, указывает метод POST и путь
# "/" — путь относительно префикса (/parts + / = /parts/)
# Т.е. полный путь будет: /parts/
# response_model=PartResponse — указывает схему ответа
# part: PartCreate — параметр запроса, автоматически валидируется
@router.post("/", response_model=PartResponse)
async def create_part(part: PartCreate):
    """Создать новую запчасть"""
    # 1. Добавляем запчасть в гараж
    garage.add_part(part.name, part.part_number, part.quantity)

    # 2. Находим только что созданную запчасть
    # (последняя в списке, так как add_part добавляет в конец)
    created_part = garage.parts[-1]

    # 3. Возвращаем созданную запчасть
    return {
        "id": created_part.id,
        "name": created_part.name,
        "part_number": created_part.part_number,
        "quantity": created_part.quantity,
    }


# 6. ПОДКЛЮЧЕНИЕ РОУТЕРА К ПРИЛОЖЕНИЮ
# Без этой строки роутер не будет работать!
app.include_router(router)


# 7. КОРНЕВОЙ ЭНДПОИНТ (GET /)
# Возвращает информацию об API
@app.get("/")
def read_root() -> Dict[str, Any]:  # для формирования документации
    """Основная страница API с информацией о доступных эндпоинтах"""
    return {
        "message": "Garage API работает!",
        "endpoints": {
            "parts_list": "/parts",
            "health_check": "/health",
            "docs": "/docs",
        },
    }


# 8. ЭНДПОИНТ ПРОВЕРКИ ЗДОРОВЬЯ (GET /health)
# Используется для мониторинга
@app.get("/health")
def health_check() -> Dict[str, Any]:  # для формирования документации
    """Проверка состояния сервиса (используется системами мониторинга)"""
    return {
        "status": "OK",
        "total_parts": len(garage.list_parts()),  # Считаем запчасти
        "service": "garage-api",
        "version": "0.1.0",
    }


# 9. ЭНДПОИНТ СПИСКА ЗАПЧАСТЕЙ (GET /parts)
# Возвращает все запчасти в формате JSON
@app.get("/parts")
def list_parts() -> Dict[str, Any]:  # для формирования документации
    parts = garage.list_parts()

    # Преобразуем объекты Part в словари
    parts_list = []
    for part in parts:
        parts_list.append(
            {
                "id": part.id,
                "name": part.name,
                "part_number": part.part_number,
                "quantity": part.quantity,
            }
        )

    return {"total": len(parts_list), "parts": parts_list}


# 10. ЭНДПОИНТ ПОЛУЧЕНИЯ КОНКРЕТНОЙ ЗАПЧАСТИ (GET /parts/{part_id})
# {part_id} — path parameter (параметр пути)
@app.get("/parts/{part_id}")
def get_part(part_id: int):
    part = garage.find_part(part_id)
    if not part:
        # HTTPException — исключение, которое превращается в HTTP ошибку
        raise HTTPException(
            status_code=404, detail=f"Запчасть с ID {part_id} не найдена"
        )
    return part  # FastAPI автоматически конвертирует в JSON


# 11. ЗАПУСК СЕРВЕРА (если файл запущен напрямую)
# Как работает: Запускается веб-сервер (uvicorn), который начинает "слушать" порт 8000
# Время жизни: Сервер работает бесконечно (пока его не остановят), ожидая HTTP-запросы
# Пример из жизни: Открыл магазин и ждешь клиентов 24/7
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
