// 2025.09.16 12:27 IMM - Аналог Python кода на C#

// Простое приложение для учета запчастей в гараже.
// (Временная версия без веб-интерфейса)
//
// В C# многострочные комментарии создаются через // или /* */
// Аналог docstring в Python, но без поддержки автоматической генерации документации

using System;
using System.Collections.Generic;

// Пространство имен GarageApp - аналог Python модуля
// Группирует связанные классы и предотвращает конфликты имен
namespace GarageApp
{
    // Класс Part (Запчасть)
    // public - модификатор доступа, означает что класс доступен из других сборок
    // В Python все классы по умолчанию public
    public class Part
    {
        // Свойства класса с автоматическими геттерами и сеттерами
        // Аналог полей класса в Python, но с дополнительной инкапсуляцией
        public int Id { get; set; }             // Уникальный идентификатор запчасти
        public string Name { get; set; }        // Название запчасти
        public string PartNumber { get; set; }  // Каталожный номер
        public int Quantity { get; set; }       // Количество на складе

        // Конструктор класса - аналог __init__ в Python
        // Вызывается при создании нового объекта через new Part(...)
        public Part(int id, string name, string partNumber, int quantity)
        {
            // Инициализация свойств значениями, переданными в конструктор
            // В C# для обращения к текущему объекту используется неявное this,
            // но можно использовать и явное this.Id = id для ясности
            Id = id;
            Name = name;
            PartNumber = partNumber;
            Quantity = quantity;
        }

        // Переопределение метода ToString() - аналог __str__ в Python
        // Определяет, как объект будет преобразован в строку при вызове Console.WriteLine
        public override string ToString()
        {
            // Интерполяция строк (аналог f-строк в Python)
            // Выражения в фигурных скобках {} вычисляются и подставляются в строку
            return $"Part(Id={Id}, Name={Name}, PartNumber={PartNumber}, Quantity={Quantity})";
        }
    }

    // Класс Garage (Гараж) представляет собой "репозиторий" или "сервис" для управления запчастями
    public class Garage
    {
        // Поле для хранения списка запчастей
        // List<Part> - универсальный список (аналог list в Python)
        // private - модификатор доступа, означает что поле доступно только внутри класса
        private List<Part> parts;

        // Счетчик для автоматической генерации уникальных ID для новых запчастей
        private int nextId = 1;

        // Конструктор класса - аналог __init__ в Python
        public Garage()
        {
            // Инициализируем пустой список для хранения всех запчастей
            parts = new List<Part>();
        }

        // Метод для добавления новой запчасти
        public Part AddPart(string name, string partNumber, int quantity)
        {
            // Создаем новый объект Part, передавая текущий nextId в качестве ID
            Part part = new Part(nextId, name, partNumber, quantity);

            // Добавляем созданный объект в список parts
            // Add - аналог append() для List<T> в C#
            parts.Add(part);

            // Увеличиваем счетчик ID для следующей запчасти
            nextId++;

            // Возвращаем созданный объект вызывающему коду
            return part;
        }

        // Метод для получения списка всех запчастей
        public List<Part> ListParts()
        {
            // Просто возвращаем весь список parts
            return parts;
        }

        // Метод для поиска запчасти по её ID
        // Part? - nullable тип (может возвращать null)
        // Аналог возврата None в Python
        public Part FindPart(int partId)
        {
            // Проходим циклом foreach по всем запчастям в списке parts
            // Цикл foreach в C# похож на for в Python
            foreach (Part part in parts)
            {
                // Если ID текущей запчасти в цикле совпадает с искомым...
                if (part.Id == partId)
                {
                    // ...возвращаем эту запчасть
                    return part;
                }
            }

            // Если цикл завершился, а запчасть не найдена, возвращаем null (аналог None в C#)
            return null;
        }
    }

    // Главный класс программы с точкой входа
    // В C# точка входа - явно определенный метод Main в классе Program
    internal class Program
    {
        // Статический метод Main - главная точка входа в наше консольное приложение
        // Аналог if __name__ == "__main__" в Python
        // static - означает, что метод принадлежит классу, а не экземпляру класса
        // void - означает, что метод не возвращает значение
        // string[] args - аргументы командной строки (аналог sys.argv в Python)
        static void Main(string[] args)
        {
            // Создаем экземпляр (объект) класса Garage. Вызывается конструктор
            // var - неявная типизация (компилятор сам определяет тип)
            var garage = new Garage();

            // Добавляем несколько запчастей в гараж, вызывая метод AddPart
            // Т.к. мы не используем базу данных, они будут храниться только в оперативной памяти
            garage.AddPart("Масляный фильтр", "OC 90", 5);
            garage.AddPart("Воздушный фильтр", "AF 123", 3);
            garage.AddPart("Свеча зажигания", "SP 456", 10);

            // Выводим заголовок в консоль
            // Console.WriteLine - аналог print() в Python
            Console.WriteLine("Запчасти в гараже:");
            Console.WriteLine("=================");

            // Получаем список всех запчастей и в цикле выводим каждую
            // Метод ListParts возвращает список, цикл foreach перебирает его элементы
            foreach (Part part in garage.ListParts())
            {
                // Для каждого объекта part вызывается его метод ToString, и результат выводится в консоль
                Console.WriteLine(part);
            }

            // Пробуем найти одну запчасть по ID
            Console.WriteLine("\nПоиск запчасти с ID=2:");

            // Вызываем метод поиска
            Part found = garage.FindPart(2);

            // Проверяем, был ли результат поиска успешным (т.е. found не равен null)
            if (found != null)
            {
                // Если нашли, выводим её
                // При передаче объекта в Console.WriteLine неявно вызывается его метод ToString
                Console.WriteLine(found);
            }
            else
            {
                // Если не нашли, выводим сообщение
                Console.WriteLine("Запчасть не найдена");
            }

            // Ожидаем нажатия любой клавиши перед закрытием консоли
            // Аналог input() в Python для паузы перед завершением
            Console.WriteLine("\nНажмите любую клавишу для выхода...");
            Console.ReadKey();
        }
    }
}