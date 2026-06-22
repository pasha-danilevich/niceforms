"""Пример формы со сложными типами данных.

Что внутри:

Enum (статусы)
Вложенные модели (Address)
Списки (tags)
Даты (date, datetime)
Валидации (ge, le, StrictInt и т.д.)

Что полезного показывает:

Что niceforms умеет работать не только с простыми полями
Как автоматически рендерятся разные типы данных"""

import datetime
from enum import Enum
from typing import List, Optional

from ._layout import base, TheNavigation
from nicegui import APIRouter, ui
from pydantic import BaseModel, Field, StrictInt

from niceforms import BaseModelForm

router = APIRouter()


class Status(str, Enum):
    SUCCESS = 'success'
    ERROR = 'error'
    WARNING = 'warning'
    INACTIVE = 'inactive'


class Address(BaseModel):
    street: str
    city: str
    index: str | int

class Person(BaseModel):
    name: str
    age: int
    index: str | int

class UserForm(BaseModel):
    """User form model for demonstration."""

    name: Optional[str] = "name"
    email: str = Field(..., title="Email", description="Введите ваш email")
    age: int = Field(..., title="Возраст", ge=18, le=100)
    summa: float = Field(..., title="Сумма")
    index: str | int
    is_active: bool = Field(True, title="Активный пользователь")
    status: Status = Field(Status.INACTIVE, title="Статус")
    address: Optional[Address] = Field(..., title="Адрес")
    tags: List[str] = Field(title="Теги")
    date: Optional[datetime.date] = Field(..., title="Дата")
    friends: list[Person]
    created_at: datetime.datetime = Field(..., title="Время создания")


@router.page('/disable_widget')
@base
async def disable_widget() -> None:
    with ui.column().classes('w-full max-w-2xl mx-auto'):
        TheNavigation(
            description='Можно делать виджеты неактивными'
        ).render()

        async def submit_handler(model: UserForm):
            print(f"Пользователь создан: {model}")

        form = BaseModelForm(UserForm, on_submit=submit_handler, view_type_error_message=False, view_annotation_type=False)
        form.render()
        form.set_enabled(False)

        form.fill({'created_at': datetime.datetime.now()})
