# scripts/setup.py
"""
Установка всех зависимостей проекта
"""

import subprocess


def run_command(command: str, description: str) -> bool:
    """Выполняет команду и выводит результат"""
    print(f"\n🔧 {description}...")
    print(f"   Команда: {command}")

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Успешно")
            if result.stdout:
                print(f"   Вывод: {result.stdout[:200]}...")
            return True
        else:
            print(f"   ❌ Ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
        return False


def main():
    print("🚀 Установка зависимостей проекта Garage API")
    print("=" * 50)

    # 1. Создание виртуального окружения (если нет)
    print("\n1. Проверка виртуального окружения...")
    import os

    venv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "venv")

    if not os.path.exists(venv_path):
        print("   ❌ Виртуальное окружение не найдено")
        create = input("   Создать виртуальное окружение? (y/n): ")
        if create.lower() == "y":
            run_command("python -m venv venv", "Создание виртуального окружения")
    else:
        print("   ✅ Виртуальное окружение найдено")

    # 2. Активация и установка зависимостей
    print("\n2. Установка зависимостей...")

    dependencies = [
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "requests",
        "pytest",
        "httpx",
    ]

    for dep in dependencies:
        run_command(f"pip install {dep}", f"Установка {dep}")

    print("\n" + "=" * 50)
    print("🎉 Установка завершена!")
    print("\n💡 Команды для запуска:")
    print("   Активация окружения: venv\\Scripts\\Activate.ps1")
    print("   Запуск сервера: python run.py")
    print("   Тестирование: python scripts/test_full_api.py")


if __name__ == "__main__":
    main()
