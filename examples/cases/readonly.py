from datetime import datetime, date
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
    birthday: Optional[datetime] = datetime.now()
    start_dt: Optional[date] = datetime.now()


@router.page('/readonly')
@base
async def basic() -> None:
    with ui.column().classes('w-full max-w-xl mx-auto'):
        TheNavigation(
            description='Пример применения свойства readonly к виджетам'
        ).render()

        async def submit_handler(model: User) -> None:
            print(f"Пользователь создан: {model}")

        form = BaseModelForm(User, on_submit=submit_handler, view_annotation_type=False)
        form.wrapper_classes = form.wrapper_classes + ' max-w-xl'
        form.render()

        form.set_readonly(True)
        form.widgets["start_dt"].set_readonly(True)