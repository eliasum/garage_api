# 2026.01.13 12:22 IMM

# РОУТЕР ДЛЯ ЗАПЧАСТЕЙ

from typing import Any, Dict

from sqlalchemy.orm import Session

from app.database import garage  # Импортируем ОДИН экземпляр
from app.db.database import get_db
from app.db.models import PartDB
from app.schemas.part import PartCreate, PartResponse  # Импортируем из папки schemas
from fastapi import APIRouter, Depends, HTTPException

# СОЗДАНИЕ РОУТЕРА ДЛЯ ЗАПЧАСТЕЙ
# APIRouter — группа эндпоинтов
# prefix="/parts" — все эндпоинты будут начинаться с /parts
# tags=["parts"] — группа в документации Swagger
router = APIRouter(prefix="/parts", tags=["parts"])


# ✅ Dependency Injection БЕЗ ЦИКЛИЧЕСКОГО ИМПОРТА
def get_garage():
    """Возвращает общий экземпляр garage"""
    return garage  # Просто возвращаем импортированный объект


# ЭНДПОИНТ СОЗДАНИЯ ЗАПЧАСТИ (POST)
# @router.post — декоратор, указывает метод POST и путь
# "/" — путь относительно префикса (/parts + / = /parts/)
# Т.е. полный путь будет: /parts/
# response_model=PartResponse — указывает схему ответа
# part: PartCreate — параметр запроса, автоматически валидируется
@router.post("/", response_model=PartResponse)
async def create_part(
    part: PartCreate,
    garage_instance=Depends(get_garage),  # Переименовываем, чтобы не конфликтовать
):
    """Создать новую запчасть"""  # ДОКСТРИНГ (строка документации Swagger UI)
    # 1. Добавляем запчасть в гараж
    garage_instance.add_part(part.name, part.part_number, part.quantity)

    # 2. Находим только что созданную запчасть
    # (последняя в списке, так как add_part добавляет в конец)
    created_part = garage_instance.parts[-1]

    # 3. Возвращаем созданную запчасть
    return {
        "id": created_part.id,
        "name": created_part.name,
        "part_number": created_part.part_number,
        "quantity": created_part.quantity,
    }
    # REST API Convention (соглашение):
    # Когда вы создаёте что-то через POST, сервер должен вернуть:
    # HTTP статус 201 Created (а не 200 OK)
    # Location заголовок с URL нового ресурса
    # Тело ответа с данными созданного объекта


# ЭНДПОИНТ СПИСКА ЗАПЧАСТЕЙ (GET /parts)
# Возвращает все запчасти в формате JSON
@router.get("/")
def list_parts(
    garage_instance=Depends(get_garage),
) -> Dict[str, Any]:  # для формирования документации
    parts = garage_instance.list_parts()

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


# ЭНДПОИНТ ПОЛУЧЕНИЯ КОНКРЕТНОЙ ЗАПЧАСТИ (GET /parts/{part_id})
# {part_id} — path parameter (параметр пути)
@router.get("/{part_id}")
def get_part(part_id: int, garage_instance=Depends(get_garage)):
    part = garage_instance.find_part(part_id)
    if not part:
        # HTTPException — исключение, которое превращается в HTTP ошибку
        raise HTTPException(
            status_code=404, detail=f"Запчасть с ID {part_id} не найдена"
        )
    return part  # FastAPI автоматически конвертирует в JSON


# ЭНДПОИНТ ОБНОВЛЕНИЯ КОНКРЕТНОЙ ЗАПЧАСТИ (PUT /parts/{part_id})
# {part_id} — path parameter (параметр пути)
@router.put("/{part_id}")
async def update_part(
    part_id: int, part_data: PartCreate, db: Session = Depends(get_db)
):
    """Обновить запчасть по ID"""
    db_part = db.query(PartDB).filter(PartDB.id == part_id).first()
    if not db_part:
        raise HTTPException(status_code=404, detail="Part not found")


# # РАЗБОР КОДА СОЗДАНИЯ ЗАПЧАСТИ
# # 🎯 СТРОКА 1: ДЕКОРАТОР (объявление эндпоинта)
# @router.post("/", response_model=PartResponse)
# # │      │    │            │
# # │      │    │            └─── 5. "ФОРМА ОТВЕТА" — FastAPI будет проверять,
# # │      │    │                   что ответ соответствует схеме PartResponse
# # │      │    │
# # │      │    └─── 4. ПУТЬ относительно префикса "/parts" → итоговый путь /parts/
# # │      │           "/" значит "корень префикса"
# # │      │
# # │      └─── 3. МЕТОД ЗАПРОСА — POST (создание данных)
# # │            Другие варианты: GET, PUT, DELETE, PATCH
# # │
# # └─── 2. "АТ" — символ декоратора. Декоратор = "надстройка" над функцией.
# #       Он говорит: "Эта функция — обработчик POST запросов"

# # 🎯 СТРОКА 2: ОБЪЯВЛЕНИЕ ФУНКЦИИ-ОБРАБОТЧИКА
# async def create_part(part: PartCreate):
# # │    │            │       │      │
# # │    │            │       │      └─── 9. ТИП ПАРАМЕТРА — Pydantic схема PartCreate
# # │    │            │       │           FastAPI автоматически:
# # │    │            │       │           1. Прочитает JSON из тела запроса
# # │    │            │       │           2. Проверит по схеме PartCreate
# # │    │            │       │           3. Преобразует в объект PartCreate
# # │    │            │       │           4. Передаст в функцию
# # │    │            │       │
# # │    │            │       └─── 8. ИМЯ ПАРАМЕТРА — "part" (может быть любым)
# # │    │            │
# # │    │            └─── 7. ИМЯ ФУНКЦИИ — может быть любым, но лучше осмысленным
# # │    │
# # │    └─── 6. КЛЮЧЕВОЕ СЛОВО "async" — объявляет асинхронную функцию
# # │          В FastAPI можно использовать async/await для работы с:
# # │          • Базами данных
# # │          • Другими API
# # │          • Файловой системой
# # │          Но МОЖНО и без async! Просто def create_part(part: PartCreate):
# # │
# # └─── 5. КЛЮЧЕВОЕ СЛОВО "def" — объявление функции (как в C#)

# # 🎯 СТРОКА 3: ДОКСТРИНГ (строка документации)
#     """Создать новую запчасть"""
#     # Эта строка появляется в документации Swagger UI

# # 🎯 СТРОКИ 4-6: ТЕЛО ФУНКЦИИ (логика обработки)
#     # 1. Добавляем запчасть в гараж
#     garage.add_part(part.name, part.part_number, part.quantity)
#     #    │           │   │      │   │            │   │
#     #    │           │   │      │   │            │   └─── 13. quantity из объекта part
#     #    │           │   │      │   │            └─── 12. обращаемся к полю part_number
#     #    │           │   │      │   └─── 11. ОБЪЕКТ part (создан FastAPI из JSON)
#     #    │           │   │      └─── 10. МЕТОД add_part класса Garage
#     #    │           │   └─── 9. обращаемся к полю name объекта part
#     #    │           └─── 8. ГЛОБАЛЬНАЯ переменная garage (создана в начале main.py)
#     #    └─── 7. ВЫЗОВ МЕТОДА — добавляем запчать в список

#     # 2. Находим только что созданную запчасть
#     created_part = garage.parts[-1]
#     #                  │       │
#     #                  │       └─── 15. ИНДЕКС -1 = последний элемент списка
#     #                  └─── 14. СПИСОК parts внутри объекта garage

#     # 3. Возвращаем созданную запчасть
#     return {
#         "id": created_part.id,
#         "name": created_part.name,
#         "part_number": created_part.part_number,
#         "quantity": created_part.quantity,
#     }
#     # FastAPI автоматически преобразует этот словарь в JSON
#     # и отправит клиенту с HTTP статусом 200 OK

# Как выглядит полный запрос в браузере:

# 1. Браузер → http://localhost:8000/parts/
# 2. FastAPI ищет: "Кто обрабатывает POST /parts/?"
# 3. Находит: "А, это функция create_part в роутере с префиксом /parts!"
# 4. Читает JSON из тела запроса
# 5. Валидирует его через PartCreate схему
# 6. Вызывает функцию create_part
# 7. Возвращает результат как JSON
