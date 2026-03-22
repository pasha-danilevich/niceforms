import logging
from enum import Enum
from types import NoneType, UnionType
from typing import Type, Any, get_type_hints
from typing import Union, get_origin, get_args

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class NormalizedType(BaseModel):
    is_nullable: bool
    origin_type: Union[type, Any]


def normalize_type(field_type: type | UnionType) -> NormalizedType:
    origin = get_origin(field_type)
    args = get_args(field_type)

    if origin is UnionType:

        if NoneType in args:
            return NormalizedType(is_nullable=True, origin_type=field_type)
        else:
            return NormalizedType(is_nullable=False, origin_type=field_type)

    if origin is None:
        return NormalizedType(is_nullable=False, origin_type=field_type)

    if origin is Union:

        if NoneType in args:
            non_nullable = [x for x in args if x is not NoneType]
            if len(non_nullable) == 1:
                return NormalizedType(is_nullable=True, origin_type=non_nullable[0])
            return NormalizedType(is_nullable=True, origin_type=field_type)
        else:
            return NormalizedType(is_nullable=False, origin_type=field_type)

    return NormalizedType(is_nullable=False, origin_type=field_type)


def is_enum_type(field_type: type) -> bool:
    return isinstance(field_type, type) and issubclass(field_type, Enum)


class NestedModel(BaseModel):
    model: type[BaseModel]
    field_name: str

def get_nested_models(model_class: Type[BaseModel]) -> list[NestedModel]:
    """
    Находит все атрибуты переданной модели, которые являются подклассами BaseModel.

    Args:
        model_class: Класс-модель Pydantic для анализа

    Returns:
        Список классов-моделей, найденных в атрибутах
    """
    result: list[NestedModel] = []

    # Получаем аннотации типов для всех атрибутов модели
    type_hints = get_type_hints(model_class)

    for attr_name, attr_type in type_hints.items():
        # Проверяем, является ли тип подклассом BaseModel (и не равен самому BaseModel)
        if (
            isinstance(attr_type, type)
            and issubclass(attr_type, BaseModel)
            and attr_type != BaseModel
        ):
            result.append(NestedModel(model=attr_type, field_name=attr_name))

    return result
