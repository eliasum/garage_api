# debug_paths.py
import os
import sys

print("🔍 ДЕБАГ ПУТЕЙ PYTHON")
print("=" * 60)

# 1. Где находится этот файл?
print(f"1. Файл скрипта: {__file__}")
print(f"2. Директория скрипта: {os.path.dirname(__file__)}")

# 2. Текущая рабочая директория
print(f"3. Рабочая директория: {os.getcwd()}")

# 3. Где Python ищет модули?
print("\n4. Python ищет модули в (sys.path):")
for i, path in enumerate(sys.path[:5], 1):
    print(f"   {i}. {path}")
print("   ...")

# 4. Пробуем найти модуль app
print("\n5. Пробуем найти модуль 'app':")
for path in sys.path:
    app_path = os.path.join(path, "app")
    if os.path.exists(app_path):
        print(f"   ✅ Найдено в: {app_path}")
        break
else:
    print("   ❌ Не найден!")

print("=" * 60)
