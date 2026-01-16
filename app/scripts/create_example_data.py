# scripts/create_example_data.py
"""
Создание тестовых данных для API
"""

import requests

BASE_URL = "http://localhost:8000"


def create_sample_parts():
    """Создание примеров запчастей"""
    print("📦 Создание тестовых данных")
    print("=" * 40)

    sample_parts = [
        {"name": "Масляный фильтр", "part_number": "OIL-001", "quantity": 5},
        {"name": "Воздушный фильтр", "part_number": "AIR-002", "quantity": 3},
        {"name": "Свеча зажигания", "part_number": "SPK-003", "quantity": 10},
        {"name": "Тормозные колодки", "part_number": "BRK-004", "quantity": 4},
        {"name": "Аккумулятор", "part_number": "BAT-005", "quantity": 2},
        {"name": "Шина", "part_number": "TIR-006", "quantity": 8},
        {"name": "Ремень ГРМ", "part_number": "TIM-007", "quantity": 6},
        {"name": "Тормозная жидкость", "part_number": "BRF-008", "quantity": 3},
        {"name": "Антифриз", "part_number": "ANT-009", "quantity": 7},
        {"name": "Лобовое стекло", "part_number": "WIN-010", "quantity": 1},
    ]

    created = 0
    for part in sample_parts:
        try:
            response = requests.post(f"{BASE_URL}/parts/", json=part, timeout=5)
            if response.status_code == 200:
                created += 1
                print(f"✅ Создана: {part['name']}")
            else:
                print(f"❌ Ошибка: {part['name']} - {response.status_code}")
        except Exception as e:
            print(f"❌ Исключение: {part['name']} - {e}")

    print(f"\n📊 Создано {created} из {len(sample_parts)} запчастей")

    # Показываем итог
    response = requests.get(f"{BASE_URL}/parts", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"📈 Всего запчастей в системе: {data['total']}")


if __name__ == "__main__":
    create_sample_parts()
