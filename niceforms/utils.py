import logging
from types import NoneType, UnionType
from typing import Type, Any
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
