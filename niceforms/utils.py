import logging
from enum import Enum
from types import NoneType, UnionType
from typing import Any, Type, Union, get_args, get_origin, get_type_hints

from nicegui.elements.mixins.validation_element import ValidationElement
from nicegui.elements.mixins.value_element import ValueElement
from pydantic import BaseModel, ConfigDict
from pydantic.fields import FieldInfo

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
    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: type[BaseModel]
    field_name: str
    field_info: FieldInfo


def extract_model_from_type(attr_type) -> list[tuple[type[BaseModel], str]]:
    """
    Рекурсивно извлекает модели BaseModel из типа, обрабатывая Union/Optional.
    Возвращает список кортежей (модель, field_name) - field_name будет использован позже.
    """
    result = []

    # Получаем оригинальный тип и аргументы
    origin = get_origin(attr_type)

    if origin is Union or origin is UnionType:
        # Это Union/Optional тип, обрабатываем каждый аргумент
        for arg in get_args(attr_type):
            result.extend(extract_model_from_type(arg))
    elif (
        isinstance(attr_type, type)
        and issubclass(attr_type, BaseModel)
        and attr_type != BaseModel
    ):
        # Это непосредственно класс BaseModel
        result.append(attr_type)

    return result


def get_nested_models(model_class: Type[BaseModel]) -> list[NestedModel]:
    """
    Находит все атрибуты переданной модели, которые являются подклассами BaseModel.
    Работает с Optional и Union типами.
    """
    result: list[NestedModel] = []
    fields: dict[str, FieldInfo] = model_class.model_fields  # type: ignore

    # Получаем аннотации типов для всех атрибутов модели
    type_hints = get_type_hints(model_class)

    for attr_name, attr_type in type_hints.items():
        # Извлекаем модели из типа (обрабатывая Optional/Union)
        models = extract_model_from_type(attr_type)

        # Добавляем каждую найденную модель в результат
        for model in models:
            result.append(
                NestedModel(
                    model=model,  # type: ignore
                    field_name=attr_name,
                    field_info=fields[attr_name],
                )
            )

    return result


def only_validation_elements(elements: list[ValueElement]) -> list[ValidationElement]:
    result: list[ValidationElement] = []

    for el in elements:
        if isinstance(el, ValidationElement):
            result.append(el)

    return result
