from enum import StrEnum
from typing import List, Optional

from _layout import base
from nicegui import APIRouter, ui
from pydantic import BaseModel, Field, StrictInt

from niceforms import BaseModelForm

router = APIRouter()


class Status(StrEnum):
    SUCCESS = 'success'
    ERROR = 'error'
    WARNING = 'warning'
    INACTIVE = 'inactive'


class Address(BaseModel):
    street: str
    city: str


class UserForm(BaseModel):
    """User form model for demonstration."""

    name: Optional[str]
    email: str = Field(..., title="Email", description="Введите ваш email")
    age: int = Field(..., title="Возраст", ge=18, le=100)
    summa: float = Field(..., title="Сумма")
    exp: StrictInt
    is_active: bool = Field(True, title="Активный пользователь")
    status: Status = Field(Status.INACTIVE, title="Статус")
    address: Optional[Address] = Field(..., title="Адрес")
    tags: List[str] = Field(title="Теги")


@router.page('/complex_type')
@base
async def complex_type() -> None:

    ui.link(text='Назад', target='/')

    async def submit_handler(user):
        print(f"Пользователь создан: {user}")

    form = BaseModelForm(UserForm, on_submit=submit_handler)
    form.render()
