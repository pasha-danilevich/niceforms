

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


@router.page('/as_dialog')
@base
async def as_dialog() -> None:
    with ui.column().classes('w-full max-w-xl mx-auto'):
        TheNavigation(
            description='Это твоя точка входа. С этого нужно начинать.'
        ).render()

        async def submit_handler(model: User) -> None:
            print(f"Пользователь создан: {model}")

        form = BaseModelForm(User, on_submit=submit_handler, view_annotation_type=False)
        form.wrapper_classes = form.wrapper_classes + ' max-w-xl'
        dialog = form.render(wrap='dialog')
        
        ui.button('Open', on_click=dialog.open)
