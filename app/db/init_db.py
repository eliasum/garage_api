# 2026.03.18 18:26 IMM

# app/db/init_db.py
import os
import sys

# Добавляем корень проекта в путь для корректных импортов
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.database import engine
from app.db.models import Base


def init_database():
    """Создаёт все таблицы в базе данных."""
    print("🚀 Создание таблиц в базе данных...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы успешно созданы.")


if __name__ == "__main__":
    init_database()
