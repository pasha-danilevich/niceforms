"""Самый простой пример использования niceforms.

Что происходит:

Есть Pydantic-модель User
На её основе строится форма
При отправке выводится результат

Что полезного показывает:

Базовый сценарий: модель → форма → submit
Как подключить BaseModelForm"""

from enum import Enum
from typing import Optional

from ._layout import base, TheNavigation
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
        TheNavigation(
            description='Это твоя точка входа. С этого нужно начинать.'
        ).render()

        async def submit_handler(model: User) -> None:
            print(f"Пользователь создан: {model}")

        form = BaseModelForm(User, on_submit=submit_handler, view_annotation_type=False)
        form.render()
