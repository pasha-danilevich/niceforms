from typing import Optional

import pytest
from pydantic import BaseModel
from utils import is_list_basemodel_type


class Person(BaseModel):
    name: str
    age: int


class TestIsListBasemodelType:

    def test_list_of_person_returns_true(self):
        """Проверка, что list[Person] возвращает True"""
        assert is_list_basemodel_type(list[Person]) is True

    def test_list_of_basemodel_returns_true(self):
        """Проверка, что list[BaseModel] возвращает True"""
        assert is_list_basemodel_type(list[BaseModel]) is True

    def test_list_of_int_returns_false(self):
        """Проверка, что list[int] возвращает False"""
        assert is_list_basemodel_type(list[int]) is False

    def test_list_of_str_returns_false(self):
        """Проверка, что list[str] возвращает False"""
        assert is_list_basemodel_type(list[str]) is False

    def test_list_without_args_returns_false(self):
        """Проверка, что list без аргументов возвращает False"""
        assert is_list_basemodel_type(list) is False

    def test_person_returns_false(self):
        """Проверка, что Person возвращает False"""
        assert is_list_basemodel_type(Person) is False

    def test_str_returns_false(self):
        """Проверка, что str возвращает False"""
        assert is_list_basemodel_type(str) is False

    def test_union_with_list_person_returns_false(self):
        """Проверка, что list[Person] | None возвращает False"""
        assert is_list_basemodel_type(list[Person] | None) is False

    def test_optional_list_person_returns_false(self):
        """Проверка, что Optional[list[Person]] возвращает False"""
        assert is_list_basemodel_type(Optional[list[Person]]) is False

    def test_list_of_custom_model_returns_true(self):
        """Проверка на пользовательской модели, наследующей BaseModel"""

        class CustomModel(BaseModel):
            field: str

        assert is_list_basemodel_type(list[CustomModel]) is True

    def test_nested_list_returns_false(self):
        """Проверка, что вложенный список возвращает False"""
        assert is_list_basemodel_type(list[list[Person]]) is False

    def test_list_of_any_returns_false(self):
        """Проверка, что list[Any] возвращает False"""
        from typing import Any

        assert is_list_basemodel_type(list[Any]) is False

    def test_list_of_union_returns_false(self):
        """Проверка, что list[Union[Person, int]] возвращает False"""
        from typing import Union

        assert is_list_basemodel_type(list[Union[Person, int]]) is False
