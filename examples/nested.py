"""Базовый пример использования."""

from typing import Optional

from nicegui import APIRouter, ui
from pydantic import BaseModel, Field

from niceforms import BaseModelForm

router = APIRouter()


class Coordinates(BaseModel):
    x: float
    y: float


class Address(BaseModel):
    """Address"""

    street: str
    city: str
    # coordinates: Coordinates


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
async def nested() -> None:
    ui.query('body').style(
        'background: linear-gradient(160deg, #eff6ff 0%, #93aeff 100%);'
        'min-height: 100vh;'
    )
    ui.link(text='Назад', target='/')

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
