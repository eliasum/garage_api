# app/scripts/trace_imports.py
import sys


def simple_trace(module_name):
    """Простая и надёжная трассировка расположения модуля."""
    try:
        module = __import__(module_name)
        # 1. Покажем, где находится корень модуля/пакета
        if hasattr(module, "__file__") and module.__file__:
            print(f"🎯 Модуль '{module_name}' найден.")
            print(f"   Файл: {module.__file__}")

            # 2. Определим тип файла
            if module.__file__.endswith(".py"):
                print("   Тип: Исходный Python-код (.py)")
                # Покажем первую строку с импортом
                try:
                    with open(module.__file__, "r", encoding="utf-8") as f:
                        first_lines = [f.readline().strip() for _ in range(5)]
                        imports = [
                            l for l in first_lines if l.startswith(("import", "from"))
                        ]
                        if imports:
                            print(f"   Первые импорты: {imports[:2]}")
                except:
                    pass
            elif module.__file__.endswith((".pyd", ".so")):
                print("   Тип: Скомпилированное нативное расширение")
            elif "built-in" in str(module.__file__):
                print("   Тип: ВСТРОЕННЫЙ модуль (часть интерпретатора)")
            else:
                print(f"   Тип: Другой ({module.__file__})")

        else:
            # Случай встроенных модулей
            print(f"🎯 Модуль '{module_name}' является ВСТРОЕННЫМ (built-in).")
            print("   Он часть интерпретатора Python, у него нет отдельного файла.")

        # 3. Проверим, является ли модуль built-in через официальный список
        if module_name in sys.builtin_module_names:
            print("   ✅ Подтверждено: модуль есть в sys.builtin_module_names")

        print("-" * 50)

    except ImportError as e:
        print(f"❌ Не удалось импортировать модуль '{module_name}': {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("ТРАССИРОВКА РАСПОЛОЖЕНИЯ МОДУЛЕЙ")
    print("=" * 60)

    # Анализируем ключевые модули
    modules_to_trace = ["sys", "os", "json", "sqlalchemy", "math"]

    for mod in modules_to_trace:
        simple_trace(mod)
