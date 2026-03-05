# 2026.03.05 18:37 IMM

from app.models import Part  # импортируем модель данных


# КЛАСС Garage (БИЗНЕС-ЛОГИКА)
# Класс Garage (Гараж) представляет собой "репозиторий" или "сервис" для управления запчастями.
class Garage:
    def __init__(self):
        # Инициализируем пустой список для хранения всех запчастей.
        # Список (list) в Python - это аналог List<T> в C#. Изменяемая коллекция.
        self.parts = list()  # или [] - то же самое
        # Счетчик для автоматической генерации уникальных ID для новых запчастей.
        self.next_id = 1

    # МЕТОД ДОБАВЛЕНИЯ ЗАПЧАСТИ
    def add_part(self, name: str, part_number: str, quantity: int):
        # Создаем новый объект Part, передавая текущий next_id в качестве ID.
        part = Part(self.next_id, name, part_number, quantity)
        # Добавляем созданный объект в список parts.
        self.parts.append(part)  # append - аналог Add() для List<T> в C#.
        # Увеличиваем счетчик ID для следующей запчасти.
        self.next_id += 1

    # МЕТОД ПОЛУЧЕНИЯ СПИСКА ВСЕХ ЗАПЧАСТЕЙ
    def list_parts(self):
        # Возвращаем копию списка (чтобы нельзя было изменить оригинал)
        return self.parts.copy()

    # МЕТОД ПОИСКА ЗАПЧАСТИ ПО ID
    def find_part(self, part_id: int):
        # Проходим циклом for по всем запчастям в списке self.parts.
        # Цикл for в Python похож на foreach в C#.
        for part in self.parts:
            # Если ID текущей запчасти в цикле совпадает с искомым...
            if part.id == part_id:
                # ...возвращаем эту запчасть.
                return part
        # Если цикл завершился, а запчасть не найдена, возвращаем None (аналог null в C#).
        return None
