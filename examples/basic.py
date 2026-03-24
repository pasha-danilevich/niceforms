"""Базовый пример использования."""

from enum import StrEnum
from typing import List, Optional

from nicegui import APIRouter, ui
from pydantic import BaseModel, Field

from niceforms import constants

constants.DEFAULT_FORM_WIDTH = "max-w-4xl"

from _layout import base

from niceforms import BaseModelForm

router = APIRouter()


class Style(StrEnum):
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
    ui.link(text='Назад', target='/')

    async def submit_handler(user: BaseModel) -> None:
        print(f"Пользователь создан: {user}")

    form = BaseModelForm(User, on_submit=submit_handler, view_annotation_type=False)
    form.render()
