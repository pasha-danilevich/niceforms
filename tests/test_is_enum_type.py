from datetime import date, datetime
from enum import Enum, IntEnum, StrEnum, auto
from types import UnionType
from typing import Any, Dict, List, Optional, Union

import pytest
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo

from utils import is_enum_type


# Определяем тестовые Enum классы
class Color(StrEnum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Status(IntEnum):
    ACTIVE = 1
    INACTIVE = 2
    PENDING = 3


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# Тестовая модель со всеми возможными типами аннотаций
class TestModel(BaseModel):
    # Простые типы
    string_field: str
    int_field: int
    float_field: float
    bool_field: bool

    # Optional типы
    optional_string: Optional[str]
    optional_int: Optional[int]
    optional_enum: Optional[Color]

    # Union типы (Python 3.10+)
    union_int_str: int | str
    union_enum_none: Color | None
    union_enum_str: Color | str
    union_multiple: int | str | float | bool

    # Union через Optional (альтернативный синтаксис)
    optional_alternative: Color | None

    # List типы
    list_string: List[str]
    list_enum: List[Color]
    list_optional_enum: List[Optional[Color]]

    # Dict типы
    dict_str_int: Dict[str, int]
    dict_str_enum: Dict[str, Color]

    # Enum типы
    color: Color
    status: Status
    priority: Priority

    # Вложенные модели
    # nested: NestedModel  # можно добавить если нужно

    # Сложные типы
    any_type: Any
    union_complex: Union[Color, Status, str]

    # С полями Field
    field_with_enum: Color = Field(..., description="Enum поле")
    field_optional_enum: Optional[Color] = Field(
        None, description="Опциональное enum поле"
    )

    # С дефолтными значениями
    default_enum: Color = Color.RED

    # Datetime типы (не Enum)
    created_at: datetime
    birth_date: date


class TestIsEnumType:
    """Тесты для функции is_enum_type"""

    @pytest.mark.parametrize(
        "field_name,expected",
        [
            # Простые типы - не Enum
            ("string_field", False),
            ("int_field", False),
            ("float_field", False),
            ("bool_field", False),
            # Optional типы - не Enum (сам Optional не Enum)
            ("optional_string", False),
            ("optional_int", False),
            # Union типы - не Enum
            ("union_int_str", False),
            ("union_multiple", False),
            # List типы - не Enum
            ("list_string", False),
            ("list_enum", False),  # List[Enum] не является Enum
            ("list_optional_enum", False),
            # Dict типы - не Enum
            ("dict_str_int", False),
            ("dict_str_enum", False),
            # Enum типы - должны быть True
            ("color", True),
            ("status", True),
            ("priority", True),
            # Optional[Enum] - сам Optional не Enum, но поле содержит Enum внутри
            ("optional_enum", False),  # Optional[Color] не является Enum
            ("field_optional_enum", False),  # Optional[Color] не является Enum
            ("union_enum_none", False),  # Color | None не является Enum
            ("union_enum_str", False),  # Color | str не является Enum
            # С дефолтным значением Enum
            ("default_enum", True),
            # С полем Field
            ("field_with_enum", True),
            # Другие типы
            ("any_type", False),
            ("created_at", False),
            ("birth_date", False),
            ("union_complex", False),  # Union[Color, Status, str] не является Enum
        ],
    )
    def test_is_enum_type_on_fields(self, field_name, expected):
        """Тестируем is_enum_type на различных полях модели"""
        field_info: FieldInfo = TestModel.model_fields[field_name]
        annotation = field_info.annotation

        # Если поле Optional или Union, то annotation будет сложным типом
        # В таких случаях is_enum_type вернет False, что правильно для прямой проверки
        result = is_enum_type(annotation)
        assert (
            result == expected
        ), f"Field '{field_name}' with annotation {annotation} returned {result}, expected {expected}"

    def test_edge_cases(self):
        """Тестируем граничные случаи"""
        # Не тип
        assert is_enum_type(None) == False
        assert is_enum_type("not a type") == False
        assert is_enum_type(123) == False

        # Класс Enum
        assert is_enum_type(Color) == True
        assert is_enum_type(Status) == True
        assert is_enum_type(Priority) == True

        # Обычные классы
        class RegularClass:
            pass

        assert is_enum_type(RegularClass) == False

        # Встроенные типы
        assert is_enum_type(str) == False
        assert is_enum_type(int) == False
        assert is_enum_type(list) == False
        assert is_enum_type(dict) == False

        # Специальные типы
        import typing

        assert is_enum_type(typing.Optional) == False
        assert is_enum_type(typing.Union) == False
        assert is_enum_type(typing.List) == False


class NestedModel(BaseModel):
    nested_enum: Color
    nested_optional_enum: Optional[Status]


# Дополнительные тесты для более сложных сценариев
class TestComplexModels:
    """Тесты для сложных моделей"""

    class ComplexModel(BaseModel):
        nested: NestedModel
        list_of_nested: List[NestedModel]
        dict_of_enums: Dict[str, Priority]
        union_of_models: Union[NestedModel, Color]
        optional_complex: Optional[Union[Color, Status]]

    def test_nested_enum_fields(self):
        """Проверяем, что вложенные поля правильно определяются"""
        # Прямые поля в ComplexModel
        assert (
            is_enum_type(self.ComplexModel.model_fields["union_of_models"].annotation)
            == False
        )

        # Проверяем поля во вложенной модели
        nested_enum = self.ComplexModel.model_fields["nested"].annotation.model_fields[
            "nested_enum"
        ]
        assert is_enum_type(nested_enum.annotation) == True

        nested_optional_enum = self.ComplexModel.model_fields[
            "nested"
        ].annotation.model_fields["nested_optional_enum"]
        assert (
            is_enum_type(nested_optional_enum.annotation) == False
        )  # Optional[Status]

    def test_generic_enum_containers(self):
        """Проверяем контейнеры с Enum внутри"""
        # List[Enum] - не содержит Enum на верхнем уровне
        list_enum_field = self.ComplexModel.model_fields["list_of_nested"]
        assert is_enum_type(list_enum_field.annotation) == False

        # Dict[str, Enum]
        dict_enum_field = self.ComplexModel.model_fields["dict_of_enums"]
        assert is_enum_type(dict_enum_field.annotation) == False


if __name__ == "__main__":
    # Запускаем тесты
    pytest.main([__file__, "-v", "--tb=short"])
