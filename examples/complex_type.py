from enum import StrEnum
from typing import Optional, List

from nicegui import ui, APIRouter
from pydantic import BaseModel
from pydantic import Field, StrictInt

from _layout import base
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
    address: Address = Field(..., title="Адрес")
    tags: Optional[List[str]] = Field([], title="Теги")


@router.page('/complex_type')
@base
async def complex_type() -> None:

    ui.link(text='Назад', target='/')

    def submit_handler(user):
        print(f"Пользователь создан: {user}")

    form = BaseModelForm(UserForm, submit_callback=submit_handler)
    form.render()
