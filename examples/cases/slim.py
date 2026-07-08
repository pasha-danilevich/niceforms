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


@router.page('/inline')
@base
async def page() -> None:
    
    with ui.column().classes('w-full max-w-xl mx-auto'):
        TheNavigation(
            description='Slim'
        ).render()

        async def submit_handler(model: User) -> None:
            print(f"Пользователь создан: {model}")

        form = BaseModelForm(User, on_submit=submit_handler, view_annotation_type=False)
        form.render()

        form = BaseModelForm(
            User, on_submit=submit_handler, view_annotation_type=False, style='inline'
        )
        form.render()

        form = BaseModelForm(
            User, on_submit=submit_handler, view_annotation_type=False, style='compact'
        )
        form.render()
