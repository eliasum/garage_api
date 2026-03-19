# 2026.03.18 18:26 IMM

# app/db/init_db.py
"""
Скрипт инициализации базы данных.
Запуск: poetry run python app/db/init_db.py
"""

import os
import sys

# Добавляем корень проекта в путь Python для корректных импортов
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.database import SessionLocal, engine
from app.db.models import Base, PartDB


def init_database():
    """Создаёт все таблицы в базе данных, если их ещё нет."""
    print("🚀 Создание таблиц в базе данных...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы успешно созданы (или уже существовали).")


def add_test_data():
    """Добавляет тестовые запчасти, если таблица пуста."""
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже записи в таблице parts
        count = db.query(PartDB).count()
        if count > 0:
            print(
                f"ℹ️  В таблице уже есть {count} записей. Тестовые данные не добавлены."
            )
            return

        print("📦 Добавление тестовых данных...")
        test_parts = [
            {
                "name": "Масляный фильтр",
                "part_number": "OIL-001",
                "quantity": 5,
                "storage_location": "Стеллаж A1",
            },
            {
                "name": "Воздушный фильтр",
                "part_number": "AIR-002",
                "quantity": 3,
                "storage_location": "Стеллаж A2",
            },
            {
                "name": "Свеча зажигания",
                "part_number": "SPK-003",
                "quantity": 10,
                "storage_location": "Стеллаж B1",
            },
            {
                "name": "Тормозные колодки",
                "part_number": "BRK-004",
                "quantity": 4,
                "storage_location": "Стеллаж C1",
            },
            {
                "name": "Аккумулятор",
                "part_number": "BAT-005",
                "quantity": 2,
                "storage_location": "Стеллаж D1",
            },
        ]

        for part_data in test_parts:
            part = PartDB(**part_data)
            db.add(part)

        db.commit()
        print(f"✅ Добавлено {len(test_parts)} тестовых запчастей.")

    except Exception as e:
        print(f"❌ Ошибка при добавлении тестовых данных: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
    add_test_data()
    print("\n🎉 Инициализация базы данных завершена.")
