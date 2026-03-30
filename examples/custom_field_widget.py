from typing import Optional

from nicegui import APIRouter, ui
from nicegui.elements.mixins.validation_element import ValidationElement

from _layout import base
from niceforms import BaseModelForm
from niceforms.widget.float import FloatWidget
from niceforms.widget.integer import IntegerWidget
from niceforms.widget.list_basemodel import ListBaseModelWidget

router = APIRouter()


from pydantic import BaseModel, Field

# Model

fake_db = {'available_manufacturers': [4, 55, 3, 10, 48, 44]}


class Address(BaseModel):
    street: str
    city: str
    manufacturer_id: int = Field()


class Item(BaseModel):
    name: str
    manufacturer_id: int = Field()
    price: float = Field(ge=0, description='Price in USD')

    color: Optional[str]


class Person(BaseModel):
    name: str
    age: int
    address: Address
    items: list[Item] = Field(
        default=[Item(name='Phone', manufacturer_id=10, price=50.3, color=None)],
        description='Person objects',
    )


# Widget


class MyCustomItemListWidget(ListBaseModelWidget):
    def get_record_title(self, model: Item) -> Optional[str]:
        return f'{model.name} - {model.price}$'


class MyCustomManufacturerWidget(IntegerWidget):
    def render(self) -> ValidationElement:
        el = super().render()
        ui.label(
            text=f'Доступные ID производителей на текущий момент: {fake_db['available_manufacturers']}.'
        ).classes('text-xs').style('color: #26a69a')

        return el


# Page


@router.page('/custom_field_widget')
@base
async def list_model() -> None:
    with ui.column().classes('w-full max-w-2xl mx-auto'):
        ui.link(text='Назад', target='/')

        async def submit_handler(model: BaseModel) -> None:
            print(f"{model}")

        form = BaseModelForm(
            Person,
            on_submit=submit_handler,
            view_annotation_type=False,
            custom_field_widget={
                'Person:items': MyCustomItemListWidget,
                'Address:manufacturer_id': MyCustomManufacturerWidget,
                'Item:manufacturer_id': MyCustomManufacturerWidget,
            },
        )
        form.render()
