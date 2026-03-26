"""Базовый пример использования."""

from enum import Enum
from typing import Optional

from _layout import base
from nicegui import APIRouter, ui
from pydantic import BaseModel, Field

from niceforms import BaseModelForm

router = APIRouter()


class Style(str, Enum):
    Red = "red"
    Green = "green"
    Yellow = "yellow"


class User(BaseModel):
    """Просто пользователь"""

    name: str = Field(default='Петя', title="Имя")
    surname: str = Field(..., description="Фамилия пользователя")
    height: Optional[int]
    style: Style = Style.Yellow


@router.page('/basic')
@base
async def basic() -> None:
    with ui.column().classes('w-full max-w-2xl mx-auto'):
        ui.link(text='Назад', target='/')

        async def submit_handler(user: BaseModel) -> None:
            print(f"Пользователь создан: {user}")

        form = BaseModelForm(User, on_submit=submit_handler, view_annotation_type=False)
        form.render()
