from typing import Optional

from nicegui import APIRouter, ui

from _layout import base
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


class Address(BaseModel):
    """Address"""

    street: str
    city: str


class Room(BaseModel):
    number: int
    floor: int
    peoples: list[Person] = Field(description='List of people that are on the room.')
    address: Address = Field(description='Address of room.')


@router.page('/fill_from')
@base
async def list_model() -> None:
    with ui.column().classes('w-full max-w-2xl mx-auto'):
        ui.link(text='Назад', target='/')

        async def submit_handler(model: BaseModel) -> None:
            print(f"{model}")

        form = BaseModelForm(Room, on_submit=submit_handler, view_annotation_type=False)
        form.render()

        form.fill(
            data={
                'number': 2,
                'floor': 1,
                'peoples': [
                    {
                        'name': 'Jon',
                        'age': 24,
                        'items': None,
                    },
                    {
                        'name': 'Pablo',
                        'age': 45,
                        'items': [
                            {
                                'size': 12,
                                'color': 'red',
                            }
                        ],
                    },
                ],
                'address': {
                    'street': 'St.',
                    'city': 'St.',
                },
            }
        )

        # or python types
        # form.fill(
        #     data={
        #         'number': 2,
        #         'floor': 1,
        #         'peoples': [
        #             Person(name='Jon', age=24, items=None),
        #             Person(name='Pablo', age=45, items=[Item(size=12, color='red')]),
        #         ],
        #     }
        # )
