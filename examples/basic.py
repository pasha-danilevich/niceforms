"""Базовый пример использования."""
from enum import StrEnum
from typing import List, Optional

from nicegui import ui, APIRouter
from pydantic import BaseModel, Field
from niceforms import constants

constants.DEFAULT_FORM_WIDTH = "max-w-4xl"

from niceforms import BaseModelForm

from _layout import base

router = APIRouter()

class Style(StrEnum):
    Red = "red"
    Green = "green"
    Yellow = "yellow"

class User(BaseModel):
    """Просто пользователь"""
    name: str = Field(default='Петя', title="Имя")
    surname: str = Field(..., description="Фамилия пользователя")
    age: int | None
    height: Optional[int]
    style: Style = Style.Yellow
    tags: List[str]
    second_tags: Optional[List[str]] = Field(default=['some', 'name', 'hello'], title="Вторичные теги")



@router.page('/basic')
@base
async def basic() -> None:
    ui.link(text='Назад', target='/')

    async def submit_handler(user: BaseModel) -> None:
        print(f"Пользователь создан: {user}")

    form = BaseModelForm(User, on_submit=submit_handler)
    form.render()
