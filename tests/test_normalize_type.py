from types import NoneType
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

import pytest

from utils import normalize_type, NormalizedType

class TestNormalizeType:
    """Тесты для функции normalize_type"""

    # === Базовые тесты ===

    def test_normalize_optional_int(self):
        """Тест для Optional[int]"""
        result = normalize_type(Optional[int])
        assert result.is_nullable is True
        assert result.origin_type == int

    def test_normalize_int_or_none(self):
        """Тест для int | None"""
        result = normalize_type(int | None)
        assert result.is_nullable is True
        assert result.origin_type == (int | None)

    def test_normalize_int(self):
        """Тест для обычного int"""
        result = normalize_type(int)
        assert result.is_nullable is False
        assert result.origin_type == int

    def test_normalize_optional_list(self):
        """Тест для Optional[List[int]]"""
        result = normalize_type(Optional[List[int]])
        assert result.is_nullable is True
        assert result.origin_type == List[int]

    def test_normalize_none_or_list_dict(self):
        """Тест для None | List[Dict[str, int]]"""
        result = normalize_type(None | List[Dict[str, int]])
        assert result.is_nullable is True
        assert result.origin_type == List[Dict[str, int]]

    def test_normalize_optional_list_dict(self):
        """Тест для Optional[List[Dict[str, int]]]"""
        result = normalize_type(Optional[List[Dict[str, int]]])
        assert result.is_nullable is True
        assert result.origin_type == List[Dict[str, int]]

    # === Дополнительные тесты ===

    def test_normalize_str(self):
        """Тест для простого str"""
        result = normalize_type(str)
        assert result.is_nullable is False
        assert result.origin_type == str

    def test_normalize_optional_str(self):
        """Тест для Optional[str]"""
        result = normalize_type(Optional[str])
        assert result.is_nullable is True
        assert result.origin_type == str

    def test_normalize_str_or_none(self):
        """Тест для str | None"""
        result = normalize_type(str | None)
        assert result.is_nullable is True
        assert result.origin_type == (str | None)

    def test_normalize_optional_complex_type(self):
        """Тест для Optional[Dict[str, List[int]]]"""
        result = normalize_type(Optional[Dict[str, List[int]]])
        assert result.is_nullable is True
        assert result.origin_type == Dict[str, List[int]]

    def test_normalize_union_with_multiple_types(self):
        """Тест для Union[int, str]"""
        result = normalize_type(Union[int, str])
        assert result.is_nullable is False
        assert result.origin_type == Union[int, str]

    def test_normalize_union_with_none(self):
        """Тест для Union[int, str, None]"""
        result = normalize_type(Union[int, str, None])
        assert result.is_nullable is True
        assert result.origin_type == Union[int, str, None]

    def test_normalize_union_with_multiple_non_nullable(self):
        """Тест для Union[int, str] без None"""
        result = normalize_type(Union[int, str])
        assert result.is_nullable is False
        assert result.origin_type == Union[int, str]

    def test_normalize_nested_optional(self):
        """Тест для Optional[Optional[int]]"""
        result = normalize_type(Optional[Optional[int]])
        assert result.is_nullable is True
        assert result.origin_type == int

    def test_normalize_nested_optional_2(self):
        """Тест для Optional[Optional[int]]"""
        result = normalize_type(Optional[Optional[List[int]]])
        assert result.is_nullable is True
        assert result.origin_type == List[int]

    def test_normalize_nested_optional_3(self):
        """Тест для Optional[Optional[int]]"""
        result = normalize_type(Optional[Optional[List[Optional[int]]]])
        assert result.is_nullable is True
        assert result.origin_type == List[Optional[int]]

    def test_normalize_tuple(self):
        """Тест для tuple"""
        result = normalize_type(Tuple[int, str])
        assert result.is_nullable is False
        assert result.origin_type == Tuple[int, str]

    def test_normalize_optional_tuple(self):
        """Тест для Optional[Tuple[int, str]]"""
        result = normalize_type(Optional[Tuple[int, str]])
        assert result.is_nullable is True
        assert result.origin_type == Tuple[int, str]

    def test_normalize_set(self):
        """Тест для Set[int]"""
        result = normalize_type(Set[int])
        assert result.is_nullable is False
        assert result.origin_type == Set[int]

    def test_normalize_callable(self):
        """Тест для Callable"""
        result = normalize_type(Callable[[int], str])
        assert result.is_nullable is False
        assert result.origin_type == Callable[[int], str]

    def test_normalize_any(self):
        """Тест для Any"""
        result = normalize_type(Any)
        assert result.is_nullable is False
        assert result.origin_type == Any

    def test_normalize_optional_any(self):
        """Тест для Optional[Any]"""
        result = normalize_type(Optional[Any])
        assert result.is_nullable is True
        assert result.origin_type == Any

    def test_normalize_bool(self):
        """Тест для bool"""
        result = normalize_type(bool)
        assert result.is_nullable is False
        assert result.origin_type == bool

    def test_normalize_float(self):
        """Тест для float"""
        result = normalize_type(float)
        assert result.is_nullable is False
        assert result.origin_type == float

    def test_normalize_bytes(self):
        """Тест для bytes"""
        result = normalize_type(bytes)
        assert result.is_nullable is False
        assert result.origin_type == bytes

    def test_normalize_none_type(self):
        """Тест для NoneType"""
        result = normalize_type(NoneType)
        assert result.is_nullable is False
        assert result.origin_type == NoneType

    def test_normalize_complex_union_with_none_first(self):
        """Тест для Union[None, int, str] - None на первом месте"""
        result = normalize_type(Union[None, int, str])
        assert result.is_nullable is True
        assert result.origin_type == Union[None, int, str]

    def test_normalize_union_with_single_type(self):
        """Тест для Union[int] (редкий случай)"""
        result = normalize_type(Union[int])
        assert result.is_nullable is False
        assert result.origin_type == Union[int]

    def test_normalize_deeply_nested_generic(self):
        """Тест для глубоко вложенных generic типов"""
        from typing import Deque, FrozenSet

        complex_type = Optional[Dict[str, List[Tuple[int, Deque[FrozenSet[str]]]]]]
        result = normalize_type(complex_type)
        assert result.is_nullable is True
        assert result.origin_type == Dict[str, List[Tuple[int, Deque[FrozenSet[str]]]]]

    def test_normalize_type_var(self):
        """Тест для TypeVar"""
        from typing import TypeVar

        T = TypeVar('T')
        result = normalize_type(Optional[T])
        assert result.is_nullable is True
        assert result.origin_type == T

    def test_normalize_literal(self):
        """Тест для Literal"""
        from typing import Literal

        result = normalize_type(Literal['a', 'b', 'c'])
        assert result.is_nullable is False
        assert result.origin_type == Literal['a', 'b', 'c']

    def test_normalize_optional_literal(self):
        """Тест для Optional[Literal['a', 'b']]"""
        from typing import Literal

        result = normalize_type(Optional[Literal['a', 'b']])
        assert result.is_nullable is True
        assert result.origin_type == Literal['a', 'b']


class TestNormalizedTypeModel:
    """Тесты для модели NormalizedType"""

    def test_normalized_type_creation(self):
        """Тест создания модели NormalizedType"""
        nt = NormalizedType(is_nullable=True, origin_type=int)
        assert nt.is_nullable is True
        assert nt.origin_type == int

    def test_normalized_type_dict_conversion(self):
        """Тест преобразования в словарь"""
        nt = NormalizedType(is_nullable=False, origin_type=str)
        assert nt.model_dump() == {"is_nullable": False, "origin_type": str}


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
