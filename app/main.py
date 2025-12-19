# 2025.11.27 18:43 IMM

from typing import Any, Dict

from fastapi import FastAPI, HTTPException

from app.models import Garage

# FastAPI (реактивный, событийно-ориентированный)
# Что это: Приложение, которое ждет запросов и реагирует на них.
# Аналог из жизни: Работа курьерского сервиса. Ты ждешь заказов, и когда приходит заказ, выполняешь его.

# СОЗДАЕМ FASTAPI ПРИЛОЖЕНИЕ
app = FastAPI(title="Garage API", description="API для учета запчастей в гараже")

# СОЗДАЕМ ГЛОБАЛЬНЫЙ ЭКЗЕМПЛЯР ГАРАЖА (пока в памяти)
garage = Garage()

# ДОБАВЛЯЕМ ТЕСТОВЫЕ ДАННЫЕ (как в твоей функции main())
garage.add_part("Масляный фильтр", "OC 90", 5)
garage.add_part("Воздушный фильтр", "AF 123", 3)
garage.add_part("Свеча зажигания", "SP 456", 10)


# КОРНЕВОЙ ЭНДПОИНТ: Приветствие и информация об API для разработчиков
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


# ЭНДПОИНТ ЗДОРОВЬЯ: Для автоматического мониторинга и проверки работоспособности
@app.get("/health")
def health_check() -> Dict[str, Any]:  # для формирования документации
    """Проверка состояния сервиса (используется системами мониторинга)"""
    return {
        "status": "OK",
        "total_parts": len(garage.list_parts()),
        "service": "garage-api",
        "version": "0.1.0",
    }


@app.get("/parts")
def list_parts() -> Dict[str, Any]:
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


@app.get("/parts/{part_id}")
def get_part(part_id: int):
    part = garage.find_part(part_id)
    if not part:
        raise HTTPException(
            status_code=404, detail=f"Запчасть с ID {part_id} не найдена"
        )
    return part  # Автоматически конвертируется в JSON


# ЗАПУСК (оставляем на случай прямого запуска файла)
# Как работает: Запускается веб-сервер (uvicorn), который начинает "слушать" порт 8000
# Время жизни: Сервер работает бесконечно (пока его не остановят), ожидая HTTP-запросы
# Пример из жизни: Открыл магазин и ждешь клиентов 24/7
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
