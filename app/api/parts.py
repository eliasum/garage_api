# 2026.03.19 18:57 IMM (ОБНОВЛЕНО: теперь с БД)

# РОУТЕР ДЛЯ ЗАПЧАСТЕЙ — работа с базой данных SQLite через SQLAlchemy

from typing import Any, Dict  # List понадобится для аннотаций

from sqlalchemy.orm import Session  # Сессия SQLAlchemy

# Больше не импортируем глобальный garage!
# from app.database import garage  # ❌ УДАЛЕНО
from app.db.database import get_db  # Функция, выдающая сессию БД
from app.db.models import PartDB  # Модель SQLAlchemy (таблица parts)
from app.schemas.part import PartCreate, PartResponse  # Pydantic-схемы
from fastapi import APIRouter, Depends, HTTPException, status  # status для кодов ответа

# СОЗДАНИЕ РОУТЕРА (без изменений)
router = APIRouter(prefix="/parts", tags=["parts"])


# ==================== ЭНДПОИНТ СОЗДАНИЯ ЗАПЧАСТИ (POST) ====================
# Раньше мы использовали глобальный garage и добавляли в список в памяти.
# Теперь мы сохраняем запчасть в настоящую базу данных через SQLAlchemy.


@router.post("/", response_model=PartResponse, status_code=status.HTTP_201_CREATED)
#   │      │    │            │                           │
#   │      │    │            │                           └── 6. Код 201 = "Создано"
#   │      │    │            │                                (раньше был 200)
#   │      │    │            └── 5. По-прежнему говорим FastAPI,
#   │      │    │                 что ответ должен соответствовать PartResponse
#   │      │    └── 4. Путь "/" — как и раньше, итоговый путь /parts/
#   │      └── 3. POST — создание нового ресурса
#   └── 2. Декоратор router (тот же)
async def create_part(part: PartCreate, db: Session = Depends(get_db)):
    #    │    │            │       │      │   │    │          │
    #    │    │            │       │      │   │    │          └── 11. get_db — зависимость,
    #    │    │            │       │      │   │    │               которая даёт сессию БД
    #    │    │            │       │      │   │    └── 10. Depends — специальная функция
    #    │    │            │       │      │    │          FastAPI, вызывает get_db()
    #    │    │            │       │      │    └── 9. db — имя параметра (можно любое)
    #    │    │            │       │      │         Здесь будет сессия SQLAlchemy
    #    │    │            │       │      └── 8. part — как и раньше, валидированная схема
    #    │    │            │       └── 7. Аннотация типа PartCreate (без изменений)
    #    │    │            └── 6. Имя функции (можно оставить)
    #    │    └── 5. Ключевое слово async (можно убрать, если не нужно)
    #    └── 4. def — объявление функции
    """
    Создать новую запчасть в базе данных.
    """
    # 🆕 Часть 1: Преобразуем Pydantic-схему в объект SQLAlchemy
    #    Раньше мы писали: garage.add_part(part.name, part.part_number, part.quantity)
    #    Теперь мы работаем через модель PartDB.
    #    **part.model_dump() распаковывает словарь из полей схемы.
    #    Например, PartCreate(name="Масло", part_number="OIL-1", quantity=5)
    #    превращается в keywords: name="Масло", part_number="OIL-1", quantity=5
    db_part = PartDB(**part.model_dump())
    #    │        │      │        │
    #    │        │      │        └── 15. model_dump() — метод Pydantic v2,
    #    │        │      │             превращает схему в словарь
    #    │        │      └── 14. Оператор ** (распаковка словаря) — передаёт пары
    #    │        │                   ключ=значение как именованные аргументы
    #    │        └── 13. PartDB — класс модели SQLAlchemy (из models.py)
    #    │              У него есть конструктор, принимающий name, part_number и т.д.
    #    └── 12. db_part — объект SQLAlchemy, ещё не сохранённый в БД

    # 🆕 Часть 2: Добавляем объект в сессию (ставим в очередь на вставку)
    db.add(db_part)
    #    │   │
    #    │   └── 16. add() — метод сессии, добавляет объект в «рабочую область».
    #    │        Пока объект не сохранён в базе.
    #    └── 17. db — наша сессия

    # 🆕 Часть 3: Фиксируем транзакцию (commit)
    db.commit()
    #    │    │
    #    │    └── 18. commit() — отправляет все накопленные изменения в БД.
    #    │         Теперь запись реально появилась в таблице parts.
    #    └── 19. После commit() объект db_part получает сгенерированный ID (если был autoincrement).

    # 🆕 Часть 4: Обновляем объект из БД (чтобы получить, например, ID)
    db.refresh(db_part)
    #    │      │
    #    │      └── 20. refresh() — перечитывает объект из базы,
    #    │           чтобы db_part.id стал актуальным (и любые другие поля,
    #    │           которые могли быть установлены БД, например, default-значения).
    #    └── 21. Теперь db_part содержит все поля, как в таблице.

    # 🆕 Часть 5: Возвращаем объект
    return db_part
    #    │
    #    └── 22. FastAPI автоматически преобразует SQLAlchemy-объект в dict,
    #         затем в JSON, используя схему PartResponse (указали в response_model).
    #         Для этого в PartResponse мы добавили class Config: from_attributes = True
    #         (см. app/schemas/part.py). Это позволяет Pydantic читать поля из ORM-объектов.

    # 🎉 ИТОГ: Теперь при POST запросе запчасть сохраняется в файл garage.db,
    #   и после перезапуска сервера данные не теряются.


# ==================== ЭНДПОИНТ СПИСКА ЗАПЧАСТЕЙ (GET /parts) ====================
# Раньше мы брали данные из garage.list_parts(). Теперь читаем из БД.


@router.get("/")
def list_parts(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Получить список всех запчастей из БД.
    """
    # 1. Выполняем запрос к таблице parts через сессию.
    #    db.query(PartDB) — создаёт запрос к таблице, связанной с моделью PartDB.
    #    .all() — выполняет запрос и возвращает ВСЕ записи в виде списка объектов PartDB.
    parts = db.query(PartDB).all()
    #    │      │      │        │
    #    │      │      │        └── 3. .all() — список всех объектов
    #    │      │      └── 2. PartDB — модель, указываем какую таблицу хотим выбрать
    #    │      └── 1. db.query() — создаём объект запроса
    #    └── 4. parts — теперь это список экземпляров PartDB, каждый соответствует строке в БД.

    # 2. Преобразуем ORM-объекты в словари (как и раньше, но теперь из PartDB)
    parts_list = []
    for part in parts:
        parts_list.append(
            {
                "id": part.id,
                "name": part.name,
                "part_number": part.part_number,
                "quantity": part.quantity,
                "storage_location": part.storage_location,  # новое поле (может быть None)
            }
        )
    #    В цикле мы обращаемся к атрибутам SQLAlchemy-объекта part.
    #    Эти атрибуты соответствуют колонкам таблицы.

    return {"total": len(parts_list), "parts": parts_list}
    # Возвращаем такой же формат, как и раньше, чтобы не ломать фронтенд (если он есть).


# ==================== ЭНДПОИНТ ПОЛУЧЕНИЯ КОНКРЕТНОЙ ЗАПЧАСТИ (GET /parts/{part_id}) ====================


@router.get("/{part_id}")
def get_part(part_id: int, db: Session = Depends(get_db)):
    """
    Получить запчасть по ID.
    """
    # Ищем одну запись с указанным ID.
    # .filter(PartDB.id == part_id) — условие WHERE id = part_id
    # .first() — возвращает первый результат или None, если ничего не найдено.
    part = db.query(PartDB).filter(PartDB.id == part_id).first()

    if not part:
        # Если запчасти нет — 404 ошибка (как и раньше)
        raise HTTPException(
            status_code=404, detail=f"Запчасть с ID {part_id} не найдена"
        )

    return part  # FastAPI преобразует в JSON автоматически


# ==================== ЭНДПОИНТ ОБНОВЛЕНИЯ ЗАПЧАСТИ (PUT /parts/{part_id}) ====================
# Ранее его не было, но сейчас добавляем для полноты.


@router.put("/{part_id}", response_model=PartResponse)
def update_part(part_id: int, part_data: PartCreate, db: Session = Depends(get_db)):
    """
    Обновить запчасть по ID (полная замена).
    """
    # 1. Находим существующую запчасть
    db_part = db.query(PartDB).filter(PartDB.id == part_id).first()
    if not db_part:
        raise HTTPException(
            status_code=404, detail=f"Запчасть с ID {part_id} не найдена"
        )

    # 2. Обновляем поля объекта данными из part_data
    #    model_dump() даёт словарь, например {"name": "...", "part_number": "...", "quantity": 5}
    #    Проходим по каждому ключу и устанавливаем новое значение в db_part
    for key, value in part_data.model_dump().items():
        setattr(
            db_part, key, value
        )  # setattr(obj, "name", value) эквивалентно obj.name = value

    # 3. Сохраняем изменения в БД
    db.commit()
    db.refresh(db_part)  # обновляем объект (на всякий случай, если были триггеры в БД)

    return db_part


# ==================== ЭНДПОИНТ УДАЛЕНИЯ ЗАПЧАСТИ (DELETE /parts/{part_id}) ====================


@router.delete("/{part_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_part(part_id: int, db: Session = Depends(get_db)):
    """
    Удалить запчасть по ID.
    """
    db_part = db.query(PartDB).filter(PartDB.id == part_id).first()
    if not db_part:
        raise HTTPException(
            status_code=404, detail=f"Запчасть с ID {part_id} не найдена"
        )

    db.delete(db_part)  # помечаем объект на удаление
    db.commit()  # фиксируем транзакцию (удаление происходит здесь)

    # Возвращаем None — для 204 ответа тело не требуется
    return None


# ==================== КОММЕНТАРИИ К ИЗМЕНЕНИЯМ ====================
# Что изменилось по сравнению со старой версией (где был garage):
#
# 1. Вместо глобального объекта garage теперь используется сессия БД (db),
#    которую мы получаем через Depends(get_db).
#
# 2. Вместо методов garage.add_part, garage.list_parts и т.д. мы используем
#    SQLAlchemy-методы: db.add(), db.commit(), db.refresh(), db.query().
#
# 3. Все объекты, которые мы сохраняем и читаем — это экземпляры модели PartDB,
#    а не старого класса Part из app.models.
#
# 4. При создании (POST) мы:
#    - Преобразуем Pydantic-схему в словарь через .model_dump()
#    - Создаём объект PartDB с распаковкой словаря: PartDB(**part.model_dump())
#    - Добавляем в сессию, коммитим, обновляем (refresh) и возвращаем.
#
# 5. При чтении списка (GET /parts/) мы выполняем запрос .all() и преобразуем
#    результат в тот же формат словаря, что и раньше, чтобы не ломать API.
#
# 6. Для PUT и DELETE добавил соответствующие эндпоинты (ранее их не было).
#
# 7. В ответах теперь может появиться поле storage_location (если оно заполнено).
#    В старом garage его не было — теперь оно есть в базе (см. models.py).
