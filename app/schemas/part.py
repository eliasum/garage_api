from pydantic import BaseModel, Field


class PartBase(BaseModel):
    """Базовая схема с общими полями"""

    name: str = Field(
        ..., min_length=1, max_length=100, description="Название запчасти"
    )
    part_number: str = Field(
        ...,
        pattern=r"^[A-Z]{3}-\d{3}$",
        description="Каталожный номер в формате ABC-123",
    )
    quantity: int = Field(default=1, gt=0, description="Количество на складе")


class PartCreate(PartBase):
    """Схема для СОЗДАНИЯ запчасти (наследует PartBase)"""

    pass  # Можно добавить специфичные для создания поля


class PartResponse(PartBase):
    """Схема для ОТВЕТА API (наследует PartBase + добавляет id)"""

    id: int

    class Config:
        from_attributes = True  # Для совместимости с ORM (например, SQLAlchemy)
