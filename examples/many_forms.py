"""Базовый пример использования."""

from enum import Enum
from typing import Optional

from nicegui import APIRouter, ui
from pydantic import BaseModel, Field

from niceforms import constants, FormError

constants.DEFAULT_FORM_WIDTH = "max-w-4xl"

from _layout import base

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

class Person(BaseModel):
    id: int
    age: int


class ApiDTO(BaseModel):
    user: User
    person: Person


@router.page('/many_forms')
@base
async def basic() -> None:
    
    
    async def submit_handler(user: BaseModel) -> None:
        print(f"Пользователь создан: {user}")
        
    with ui.column().classes('w-full max-w-2xl mx-auto'):
        ui.link(text='Назад', target='/')
        
        user_form = BaseModelForm(User, on_submit=submit_handler, view_annotation_type=False)
        user_form.render()
        person_form = BaseModelForm(Person, on_submit=submit_handler, view_annotation_type=False)
        person_form.render()
        
        
        def collect_all_forms() -> None:
            try:
                user = User(**user_form.collect_form_data().model_dump())
                person = Person(**person_form.collect_form_data().model_dump())
            except FormError:
                return
            
            dto = ApiDTO(
                user=user,
                person=person
            )
            print(f'Отправить DTO бэкенду: {dto.model_dump()}')
        
        ui.button('Отправить', on_click=collect_all_forms)