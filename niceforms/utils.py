from typing import Type, Union, List

from typing import Union, get_origin, get_args


def normalize_type(field_type: type):
    """Приводит различные представления типов к единому виду"""
    # Если это параметризованный тип (list[str], List[str] и т.д.)
    origin = get_origin(field_type)
    if origin is not None:
        # Для других generic типов можно добавить обработку
        return origin

    return field_type

class TypeProcessor:
    """Utility class for type processing and validation."""

    @staticmethod
    def is_optional_type(field_type: Type) -> bool:
        """Check if a type is Optional (Union[type, None]).

        Args:
            field_type: Type to check

        Returns:
            True if the type is Optional, False otherwise
        """
        origin = getattr(field_type, "__origin__", None)

        if origin is Union:
            args = field_type.__args__
            return type(None) in args

        return False

    @staticmethod
    def get_base_type(field_type: Type) -> Type:
        """Extract the base type from Optional[...].

        Args:
            field_type: Type to process

        Returns:
            Base type without None
        """
        if TypeProcessor.is_optional_type(field_type):
            args = field_type.__args__
            non_none_types = [arg for arg in args if arg != type(None)]
            return non_none_types[0] if non_none_types else field_type

        return field_type

    @staticmethod
    def is_list_type(field_type: Type) -> bool:
        """Check if a type is a List.

        Args:
            field_type: Type to check

        Returns:
            True if the type is a List, False otherwise
        """
        origin = getattr(field_type, "__origin__", None)
        return origin is list or getattr(field_type, "_name", None) == "List"