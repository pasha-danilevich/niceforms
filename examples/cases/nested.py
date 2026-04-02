"""Пример вложенных моделей (nested forms).

Что происходит:

User содержит:
Address
Coordinates
Appearance
Всё это автоматически превращается в вложенную форму

Что полезного показывает:

Как niceforms строит иерархию форм
Работа с Optional вложенными объектами"""

from typing import Optional

from nicegui import APIRouter, ui
from pydantic import BaseModel, Field

from ._layout import base, TheNavigation
from niceforms import BaseModelForm

router = APIRouter()


class Coordinates(BaseModel):
    x: float
    y: float


class Address(BaseModel):
    """Address"""

    street: str
    city: str
    coordinates: Coordinates


class Appearance(BaseModel):
    """Appearance"""

    hair: str
    color: str


class User(BaseModel):
    """Some description"""

    name: str
    age: int
    address: Optional[Address]
    appearance: Appearance = Field(
        ..., title="Внешний вид", description="Отличительные черты персоны"
    )


@router.page('/nested')
@base
async def nested() -> None:

    with ui.column().classes('w-full max-w-2xl mx-auto'):
        TheNavigation(description='Когда структура данных сложная и вложенная').render()

        async def submit_handler(user: BaseModel):
            print(f"Пользователь создан: {user.model_dump()}")

        form = BaseModelForm(
            User,
            on_submit=submit_handler,
            view_annotation_type=False,
            view_clear_button=True,
            view_json_button=False,
        )
        form.render()
