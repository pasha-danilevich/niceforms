from typing import Optional

from _layout import base
from nicegui import APIRouter, ui

from niceforms import BaseModelForm

router = APIRouter()


from pydantic import BaseModel, Field


class Item(BaseModel):
    size: int
    color: str


class Person(BaseModel):
    name: str
    age: int
    items: Optional[list[Item]] = Field(description='Person objects')


class Room(BaseModel):
    number: int
    floor: int
    peoples: list[Person] = Field(
        default=[
            Person(name='Jon', age=24, items=None),
            Person(name='Pablo', age=45, items=[Item(size=12, color='red')]),
        ],
        description='List of people that are on the room.',
    )
    # peoples: list[Person] = Field(description='List of people that are on the room.')


@router.page('/list_model')
@base
async def list_model() -> None:
    with ui.column().classes('w-full max-w-2xl mx-auto'):
        ui.link(text='Назад', target='/')

        async def submit_handler(model: BaseModel) -> None:
            print(f"{model}")

        form = BaseModelForm(Room, on_submit=submit_handler, view_annotation_type=False)
        form.render()
