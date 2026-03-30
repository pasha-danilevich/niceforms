import pytest
from typing import Any, Optional

from pydantic import BaseModel, Field

from niceforms import BaseModelForm

# Test data
case = {
    'Person:items': 1,
    'Person:name': 2,
    'Item:manufacturer_id': 3,
}


class Item(BaseModel):
    name: str
    price: float = Field(ge=0, description='Price in USD')
    manufacturer_id: int = Field()
    size: Optional[int]
    color: Optional[str]


class Person(BaseModel):
    name: str
    age: int
    items: list[Item] = Field(description='Person objects')


person_form = BaseModelForm(model=Person)
item_form = BaseModelForm(model=Item)


def test_extract_person_fields():
    """Test extracting fields for Person model"""
    result = person_form.custom_widgets(case)
    expected = {'items': 1, 'name': 2}
    assert result == expected
    assert len(result) == 2


def test_extract_item_fields():
    """Test extracting fields for Item model"""
    result = item_form.custom_widgets(case)
    expected = {'manufacturer_id': 3}
    assert result == expected
    assert len(result) == 1


def test_empty_data():
    """Test with empty dictionary"""
    result = person_form.custom_widgets({})
    expected = {}
    assert result == expected
    assert len(result) == 0


def test_partial_match():
    """Test when model name appears as substring in other keys"""
    data = {
        'Person:name': 'John',
        'Personality:type': (
            'friendly'
        ),  # Starts with 'Person' but not exactly 'Person:'
        'Person:age': 30,
    }
    result = person_form.custom_widgets(data)
    expected = {'name': 'John', 'age': 30}
    assert result == expected
    assert 'type' not in result


def test_preserves_values():
    """Test that values are preserved correctly"""
    data = {
        'Person:name': 'Alice',
        'Person:age': 25,
        'Person:active': True,
        'Person:scores': [1, 2, 3],
        'Person:data': {'key': 'value'},
    }
    result = person_form.custom_widgets(data)
    assert result['name'] == 'Alice'
    assert result['age'] == 25
    assert result['active'] is True
    assert result['scores'] == [1, 2, 3]
    assert result['data'] == {'key': 'value'}


def test_returns_new_dict():
    """Test that the function returns a new dictionary, not a view or reference"""
    data = {'Person:field': 'value'}
    result = person_form.custom_widgets(data)

    # Modify the result
    result['new_field'] = 'new_value'

    # Original data should remain unchanged
    assert data == {'Person:field': 'value'}
    assert 'new_field' not in data


def test_mixed_data_types():
    """Test with various data types in values"""
    mixed_data = {
        'Person:name': 'John Doe',
        'Person:age': 30,
        'Person:is_active': True,
        'Person:tags': ['developer', 'python'],
        'Person:profile': {'city': 'NYC', 'country': 'USA'},
        'Person:score': 95.5,
        'Person:is_verified': False,
    }

    result = person_form.custom_widgets(mixed_data)

    assert isinstance(result['name'], str)
    assert isinstance(result['age'], int)
    assert isinstance(result['is_active'], bool)
    assert isinstance(result['tags'], list)
    assert isinstance(result['profile'], dict)
    assert isinstance(result['score'], float)
    assert isinstance(result['is_verified'], bool)
