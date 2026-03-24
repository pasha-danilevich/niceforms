"""Базовый пример использования."""

from typing import Optional

from nicegui import APIRouter, ui
from pydantic import BaseModel

from niceforms import BaseModelForm

router = APIRouter()


class Some(BaseModel):
    hello: str
    bye: str


class Address(BaseModel):
    """Some description"""

    street: str
    city: str
    some: Some


class User(BaseModel):
    """Some description"""

    name: str
    age: int
    address: Optional[Address]


@router.page('/nested')
async def nested() -> None:
    ui.query('body').style(
        'background: linear-gradient(160deg, #eff6ff 0%, #93aeff 100%);'
        'min-height: 100vh;'
    )
    ui.link(text='Назад', target='/')

    async def submit_handler(user):
        print(f"Пользователь создан: {user}")

    form = BaseModelForm(
        User,
        on_submit=submit_handler,
        view_annotation_type=False,
        view_clear_button=False,
        view_json_button=False,
    )
    form.render()
