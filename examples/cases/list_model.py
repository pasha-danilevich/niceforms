"""Пример работы со списками вложенных моделей.

Что происходит:

В модели есть list[Person]
У каждого Person есть список Item

Что полезного показывает:

Как niceforms автоматически строит формы для списков
Как добавляются/удаляются элементы списка"""

from typing import Optional

from ._layout import base, TheNavigation
from nicegui import APIRouter, ui

from niceforms import BaseModelForm

router = APIRouter()


from pydantic import BaseModel, Field


class Item(BaseModel):
    size: int
    color: str


class Person(BaseModel):
    name: str
    age: int
    items: Optional[list[Item]] = Field(description='Person objects')


class Room(BaseModel):
    number: int
    floor: int
    peoples: list[Person] = Field(description='List of people that are on the room.')


@router.page('/list_model')
@base
async def list_model() -> None:
    with ui.column().classes('w-full max-w-2xl mx-auto'):
        TheNavigation(
            description='Когда нужно редактировать массивы объектов (например список товаров)'
        ).render()

        async def submit_handler(model: Room) -> None:
            print(f"{model}")

        form = BaseModelForm[Room](Room, on_submit=submit_handler, view_annotation_type=False)
        form.render()
