garage_api/
├── app/
│   ├── __init__.py
│   ├── main.py             # Точка входа, FastAPI-приложение
│   ├── api/
│   │   ├── __init__.py
│   │   └── parts.py        # Эндпоинты для запчастей (роутер)
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py       # Настройки (адрес БД и т.д.)
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py         # Базовая модель SQLAlchemy и сессии
│   │   └── models.py       # Модели таблиц SQLAlchemy
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── part.py         # Pydantic-схемы для валидации данных
│   └── services/
│       ├── __init__.py
│       └── parts_service.py # Бизнес-логика, CRUD-операции (Repository Pattern)
├── tests/
│   ├── __init__.py
│   └── test_parts_api.py   # Тесты для API запчастей
├── .env                    # Файл с переменными окружения (секреты)
├── .gitignore
├── docker-compose.yml      # Оркестрация контейнеров
├── Dockerfile              # Инструкция по сборке образа приложения
└── pyproject.toml          # Управление зависимостями (Poetry)