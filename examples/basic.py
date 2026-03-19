"""Базовый пример использования."""
from typing import List

from nicegui import ui, APIRouter
from pydantic import BaseModel, Field
from niceforms import constants
constants.DEFAULT_FORM_WIDTH = "max-w-4xl"

from niceforms import BaseModelForm

from _layout import base
router = APIRouter()


class User(BaseModel):
    """Просто пользователь"""
    name: str = Field(default='Петя', title="Имя")
    surname: str = Field(..., description="Фамилия пользователя")
    age: int
    # email: str
    # items: list[str]
    # items_typed: List[str] # параметризованные типы (generic types)



@router.page('/basic')
@base
async def basic() -> None:

    ui.link(text='Назад', target='/')
    def submit_handler(user):
        print(f"Пользователь создан: {user}")



    form = BaseModelForm(User, submit_callback=submit_handler)
    form.render()
