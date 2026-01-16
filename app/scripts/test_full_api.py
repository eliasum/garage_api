"""
📡 Полный тест Garage API

Перед запуском:
1. Установите requests: pip install requests
2. Запустите сервер: python run.py
3. Запустите тест: python scripts/test_full_api.py
"""

import json
import os
import sys
import time
from typing import Dict, Optional

# Добавляем корень проекта в путь Python
# Это нужно для импорта модулей проекта (если будут нужны)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    # Пытаемся импортировать requests
    import requests

    print("✅ Библиотека requests установлена")
except ImportError:
    print("❌ Библиотека requests не установлена")
    print("   Установите: pip install requests")
    sys.exit(1)

BASE_URL = "http://localhost:8000"


def test_endpoint(
    method: str,
    path: str,
    data: Optional[Dict] = None,
    expected_status: int = 200,
    description: str = "",
) -> bool:
    """
    Тестирует эндпоинт API

    Args:
        method: HTTP метод (GET, POST, PUT, DELETE)
        path: Путь эндпоинта
        data: Данные для POST/PUT запросов
        expected_status: Ожидаемый HTTP статус
        description: Описание теста для вывода

    Returns:
        bool: True если тест пройден, False если нет
    """
    if description:
        print(f"\n📌 {description}")

    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{path}", timeout=5)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{path}", json=data, timeout=5)
        elif method == "PUT":
            response = requests.put(f"{BASE_URL}{path}", json=data, timeout=5)
        elif method == "DELETE":
            response = requests.delete(f"{BASE_URL}{path}", timeout=5)
        else:
            print(f"❌ Неизвестный метод: {method}")
            return False

        success = response.status_code == expected_status
        status_icon = "✅" if success else "❌"

        print(f"{status_icon} {method} {path}")
        print(f"   Статус: {response.status_code} (ожидался: {expected_status})")

        if response.text:
            try:
                json_data = response.json()
                print(
                    f"   Ответ: {json.dumps(json_data, indent=2, ensure_ascii=False)}"
                )
            except json.JSONDecodeError:
                print(f"   Ответ (не JSON): {response.text[:100]}...")

        return success

    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {path} - Не удалось подключиться к серверу")
        print("   Убедитесь, что сервер запущен: python run.py")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ {method} {path} - Таймаут запроса")
        return False
    except Exception as e:  # ✅ Теперь не "bare except"
        print(f"❌ {method} {path} - Ошибка: {type(e).__name__}: {e}")
        return False


def test_validation() -> bool:
    """Тестирование валидации данных"""
    print("\n🧪 Тестирование валидации данных:")

    test_cases = [
        # (данные, ожидаемый статус, описание)
        ({"name": "", "part_number": "ABC-123", "quantity": 5}, 422, "Пустое имя"),
        (
            {"name": "Фильтр", "part_number": "123-ABC", "quantity": 5},
            422,
            "Неправильный формат номера",
        ),
        (
            {"name": "Фильтр", "part_number": "ABC-123", "quantity": 0},
            422,
            "Количество должно быть > 0",
        ),
        (
            {"name": "Фильтр", "part_number": "ABC-123"},
            200,  # quantity по умолчанию = 1
            "quantity по умолчанию",
        ),
    ]

    all_passed = True
    for data, expected_status, description in test_cases:
        passed = test_endpoint(
            "POST", "/parts/", data, expected_status, f"Валидация: {description}"
        )
        all_passed = all_passed and passed

    return all_passed


def main():
    """Основная функция тестирования"""
    print("🚀 Запуск полного тестирования Garage API")
    print("=" * 70)

    # 1. Проверяем запущен ли сервер
    print("1. Проверка подключения к серверу...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=3)
        if response.status_code == 200:
            print("✅ Сервер запущен и отвечает")
            print(f"   Приветствие: {response.json().get('message', '')}")
        else:
            print(f"❌ Сервер отвечает с ошибкой: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу")
        print("   Запустите сервер в отдельном терминале:")
        print("   cd C:\\dev-projects\\garage_api")
        print("   python run.py")
        return

    # 2. Тестируем основные эндпоинты
    print("\n2. Тестируем основные эндпоинты:")
    test_endpoint("GET", "/", description="Главная страница")
    test_endpoint("GET", "/health", description="Health check")
    test_endpoint("GET", "/parts", description="Список запчастей")
    test_endpoint("GET", "/parts/1", description="Конкретная запчасть (ID=1)")
    test_endpoint("GET", "/parts/999", 404, "Несуществующая запчасть")

    # 3. Тестируем создание запчасти
    print("\n3. Тестируем создание запчасти:")
    new_part = {"name": "Тормозные колодки", "part_number": "BRK-001", "quantity": 4}
    test_endpoint("POST", "/parts/", new_part, 200, "Создание новой запчасти")

    # 4. Проверяем, что запчасть добавилась
    print("\n4. Проверяем, что запчасть добавилась...")
    time.sleep(0.5)  # Даём время на обработку
    response = requests.get(f"{BASE_URL}/parts", timeout=5)
    if response.status_code == 200:
        parts = response.json()
        print(f"✅ Всего запчастей: {parts['total']}")
        print(f"✅ Последняя запчасть: {parts['parts'][-1]['name']}")
        print(f"✅ Её ID: {parts['parts'][-1]['id']}")
    else:
        print("❌ Не удалось получить список запчастей")

    # 5. Тестируем валидацию
    test_validation()

    # 6. Тестируем кейз с правильными данными
    print("\n6. Тестируем создание второй запчасти:")
    second_part = {"name": "Масляный фильтр", "part_number": "OIL-001", "quantity": 10}
    test_endpoint("POST", "/parts/", second_part, 200, "Вторая запчасть")

    print("\n" + "=" * 70)
    print("🎉 Тестирование завершено!")
    print("✨ Ваш Garage API полностью работоспособен!")

    # Показываем итоговую информацию
    response = requests.get(f"{BASE_URL}/parts", timeout=5)
    if response.status_code == 200:
        parts = response.json()
        print("\n📊 Итоговая статистика:")
        print(f"   Всего запчастей в системе: {parts['total']}")
        print(f"   Примеры: {', '.join(p['name'] for p in parts['parts'][:3])}...")


if __name__ == "__main__":
    main()
