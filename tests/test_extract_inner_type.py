import pytest
from typing import List, Any
from pydantic import BaseModel

# Импортируем тестируемую функцию (предположим, она в файле utils.py)
# from utils import extract_inner_type


# Определим тестовые классы
class Item:
    def __init__(self, name: str):
        self.name = name


class Product(BaseModel):
    id: int
    name: str


class User(BaseModel):
    username: str
    email: str


# Функция для тестирования
def extract_inner_type(type_hint: Any) -> Any:
    """Извлекает внутренний тип из List/списка"""
    from typing import get_origin, get_args, List

    origin = get_origin(type_hint)

    if origin in (list, List):
        args = get_args(type_hint)
        if len(args) == 1:
            return args[0]

    return None


# ==================== ТЕСТЫ ====================


class TestExtractInnerType:
    """Тесты для функции extract_inner_type"""

    # === Тесты для встроенного list (Python 3.9+) ===

    @pytest.mark.parametrize(
        "type_hint,expected",
        [
            (list[int], int),
            (list[str], str),
            (list[float], float),
            (list[bool], bool),
            (list[Item], Item),
            (list[Product], Product),
            (list[User], User),
        ],
    )
    def test_list_builtin_with_single_type(self, type_hint, expected):
        """Тест для list[Type] с одним типом"""
        result = extract_inner_type(type_hint)
        assert result == expected

    @pytest.mark.parametrize(
        "type_hint",
        [
            list,
            list[Any],
            list[list[int]],
            list[dict[str, int]],
        ],
    )
    def test_list_builtin_various_inner_types(self, type_hint):
        """Тест для list с различными внутренними типами"""
        result = extract_inner_type(type_hint)
        if type_hint is list:
            # list без аргументов не должен возвращать None
            assert result is None
        else:
            # list[Any] или list[list[int]] должны вернуть внутренний тип
            from typing import get_args

            expected = get_args(type_hint)[0]
            assert result == expected

    # === Тесты для typing.List ===

    @pytest.mark.parametrize(
        "type_hint,expected",
        [
            (List[int], int),
            (List[str], str),
            (List[float], float),
            (List[bool], bool),
            (List[Item], Item),
            (List[Product], Product),
            (List[User], User),
        ],
    )
    def test_typing_list_with_single_type(self, type_hint, expected):
        """Тест для List[Type] с одним типом"""
        result = extract_inner_type(type_hint)
        assert result == expected

    @pytest.mark.parametrize(
        "type_hint",
        [
            List,
            List[Any],
            List[list[int]],
            List[dict[str, int]],
        ],
    )
    def test_typing_list_various_inner_types(self, type_hint):
        """Тест для List с различными внутренними типами"""
        result = extract_inner_type(type_hint)
        if type_hint is List:
            # List без аргументов не должен возвращать None
            assert result is None
        else:
            from typing import get_args

            expected = get_args(type_hint)[0]
            assert result == expected

    # === Тесты для неподдерживаемых типов ===

    @pytest.mark.parametrize(
        "type_hint",
        [
            int,
            str,
            float,
            bool,
            dict,
            dict[str, int],
            tuple,
            tuple[int, str],
            set,
            set[int],
            None,
            Item,
            Product,
            User,
            Any,
        ],
    )
    def test_non_list_types_return_none(self, type_hint):
        """Тест для типов, которые не являются списками"""
        result = extract_inner_type(type_hint)
        assert result is None

    # === Тесты для вложенных списков ===

    @pytest.mark.parametrize(
        "type_hint,expected",
        [
            (list[list[int]], list[int]),
            (List[List[str]], List[str]),
            (list[list[list[int]]], list[list[int]]),
            (List[List[List[Item]]], List[List[Item]]),
        ],
    )
    def test_nested_lists(self, type_hint, expected):
        """Тест для вложенных списков - возвращает только первый уровень"""
        result = extract_inner_type(type_hint)
        assert result == expected

    # === Тесты для смешанных типов ===

    @pytest.mark.parametrize(
        "type_hint,expected",
        [
            (list[Product], Product),
            (List[Product], Product),
            (list[Item], Item),
            (List[Item], Item),
            (list[BaseModel], BaseModel),
            (List[BaseModel], BaseModel),
        ],
    )
    def test_custom_classes_and_pydantic_models(self, type_hint, expected):
        """Тест для пользовательских классов и Pydantic моделей"""
        result = extract_inner_type(type_hint)
        assert result == expected
        # Дополнительная проверка, что это класс
        assert isinstance(result, type)

    # === Тесты для граничных случаев ===

    def test_list_with_union(self):
        """Тест для List[Union[int, str]]"""
        from typing import Union

        type_hint = List[Union[int, str]]
        result = extract_inner_type(type_hint)

        from typing import get_origin, Union as UnionType

        assert result is not None
        assert get_origin(result) is UnionType

    def test_empty_list_type(self):
        """Тест для пустого list (без аргументов)"""
        # В Python нельзя создать list[] без аргументов, но можно проверить List
        from typing import List as TypingList

        # List без аргументов (в старом синтаксисе)
        result = extract_inner_type(TypingList)
        assert result is None

        # list без аргументов (в Python 3.9+)
        result = extract_inner_type(list)
        assert result is None


# ==================== ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ ====================


class TestEdgeCases:
    """Тесты для граничных и особых случаев"""

    def test_type_alias(self):
        """Тест для type alias"""
        IntList = List[int]
        result = extract_inner_type(IntList)
        assert result == int


# ==================== ФИКСТУРЫ ДЛЯ ТЕСТОВ ====================


@pytest.fixture
def sample_classes():
    """Фикстура с тестовыми классами"""
    return {
        'item': Item,
        'product': Product,
        'user': User,
    }


def test_with_fixture(sample_classes):
    """Тест с использованием фикстуры"""
    for class_name, cls in sample_classes.items():
        type_hint = list[cls]
        result = extract_inner_type(type_hint)
        assert result == cls
        assert (
            result.__name__ == class_name.capitalize()
            if class_name != 'item'
            else 'Item'
        )


# ==================== ПАРАМЕТРИЗОВАННЫЙ КЛАСС ====================


@pytest.mark.parametrize(
    "type_hint,expected_type,expected_name",
    [
        (list[int], int, 'int'),
        (list[str], str, 'str'),
        (list[Item], Item, 'Item'),
        (List[Product], Product, 'Product'),
        (list[User], User, 'User'),
    ],
)
def test_extract_inner_type_with_names(type_hint, expected_type, expected_name):
    """Параметризованный тест с проверкой имени типа"""
    result = extract_inner_type(type_hint)
    assert result == expected_type
    if hasattr(result, '__name__'):
        assert result.__name__ == expected_name


# ==================== ЗАПУСК ТЕСТОВ ====================

if __name__ == "__main__":
    # Запуск тестов через pytest
    pytest.main([__file__, "-v", "--tb=short"])
