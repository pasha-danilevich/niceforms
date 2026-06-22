from enum import Enum
from typing import Optional

from nicegui import APIRouter, ui
from pydantic import BaseModel, Field

from niceforms import BaseModelForm
from niceforms.widget.list_basemodel import ListBaseModelWidget
from ._layout import base, TheNavigation

router = APIRouter()


class Style(str, Enum):
    Red = "red"
    Green = "green"
    Yellow = "yellow"


class Address(BaseModel):
    id: int = 0
    street: str
    city: str


class Person(BaseModel):
    """Some description"""

    id: int = 0
    name: str = Field(min_length=1, max_length=20)
    age: int


class User(BaseModel):
    """Просто пользователь"""

    id: int = 0
    name: str = Field(default='Петя', title="Имя")
    surname: str = Field(..., description="Фамилия пользователя")
    height: Optional[int]
    style: Style = Style.Yellow
    address: Address
    relations: list[Person]


def hide_id_field(widget: ListBaseModelWidget):
    
    for record in widget.column.records:
        record.edit_form.widgets['id'].set_visibility(False)
        record.read_form.widgets['id'].set_visibility(False)

def hide_delete_icon(widget: ListBaseModelWidget):
    for record in widget.column.records:
        record.delete_button.set_visibility(False)

@router.page('/widget_visibility')
@base
async def basic() -> None:
    with ui.column().classes('w-full max-w-xl mx-auto'):
        TheNavigation(
            description='Это твоя точка входа. С этого нужно начинать.'
        ).render()

        async def submit_handler(model: User) -> None:
            print(f"Пользователь создан: {model}")

        form = BaseModelForm(User, on_submit=submit_handler, view_annotation_type=False)
        form.wrapper_classes = form.wrapper_classes + ' max-w-xl'
        form.render()

        form.fill(
            {
                'relations': [
                    Person(name='Jon', age=23, id=0),
                    Person(name='Bob', age=32, id=0),
                ]
            }
        )

        form.widgets["id"].set_visibility(False)
        form.widgets["address"].form.widgets["id"].set_visibility(False)

        list_widget: ListBaseModelWidget = form.widgets["relations"]
        
        list_widget.column.add_button.set_visibility(False)
        
        hide_id_field(list_widget)
        hide_delete_icon(list_widget)

        list_widget.column.on_refresh.subscribe(
            lambda: hide_id_field(list_widget)
        )
        list_widget.column.on_refresh.subscribe(
            lambda: hide_delete_icon(list_widget)
        )
