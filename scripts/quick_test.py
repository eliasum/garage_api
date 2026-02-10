# scripts/quick_test.py
"""
Быстрый тест API (без requests)
Использует встроенный HTTP клиент
"""

import json
import urllib.request

BASE_URL = "http://localhost:8000"


def quick_test():
    """Быстрый тест без дополнительных зависимостей"""
    print("⚡ Быстрый тест Garage API")
    print("=" * 40)

    endpoints = ["/", "/health", "/parts"]

    for endpoint in endpoints:
        try:
            with urllib.request.urlopen(f"{BASE_URL}{endpoint}", timeout=5) as response:
                data = response.read().decode("utf-8")
                json_data = json.loads(data)
                print(f"✅ GET {endpoint}: {response.status}")
                if endpoint == "/parts":
                    print(f"   Запчастей: {json_data.get('total', 0)}")
        except Exception as e:
            print(f"❌ GET {endpoint}: {e}")

    print("\n" + "=" * 40)
    print("✨ API работает!")


if __name__ == "__main__":
    quick_test()
