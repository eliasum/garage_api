"""
МОДЕЛИ ДАННЫХ (Data Models)

Назначение: Этот файл определяет структуру таблиц в базе данных.
Здесь создаются Python-классы (модели), которые SQLAlchemy автоматически
преобразует в SQL-таблицы (это называется ORM - Object Relational Mapping).

Основные концепции:
- Каждый класс = отдельная таблица в БД
- Каждый атрибут класса = колонка в таблице
- Base = базовый класс, от которого наследуются все модели
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Базовый класс для всех моделей. Все таблицы регистрируются через него.
# Это "точка входа" для системы маппинга SQLAlchemy.
Base = declarative_base()


class Part(Base):
    """
    Модель 'Запчасть'. Соответствует таблице 'parts' в базе данных.
    Каждая запись в этой таблице = одна запчасть в гараже.
    """

    __tablename__ = "parts"  # Имя таблицы в SQL (обязательный атрибут)

    # Поля таблицы (колонки). Комментарии объясняют параметры Column:
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    # ↑ PRIMARY KEY, с индексом, не может быть NULL

    name = Column(String, nullable=False)
    # ↑ Название запчасти, обязательное поле (NOT NULL)

    part_number = Column(String, unique=True, index=True)
    # ↑ Уникальный каталожный номер, с индексом для быстрого поиска

    quantity = Column(Integer, default=0)
    # ↑ Количество на складе, по умолчанию = 0

    storage_location = Column(String, nullable=True)
    # ↑ Место хранения (полка, ящик), может быть не указано (NULL)

    # SQLAlchemy автоматически создаст конструктор __init__,
    # поэтому писать его вручную не нужно.
    # Также автоматически доступен метод __repr__ для отладки.
