from typing import Optional

from nicegui import APIRouter, ui
from nicegui.elements.mixins.validation_element import ValidationElement
from pydantic import BaseModel, Field

from _layout import base
from niceforms import BaseModelForm
from niceforms.widget.integer import IntegerWidget
from niceforms.widget.list_basemodel import ListBaseModelWidget

router = APIRouter()

# Model

FAKE_DB = {'available_manufacturers': [4, 55, 3, 10, 48, 44]}


class Some(BaseModel):
    id: int = Field(...)
    manufacturer_id: int = Field()


class Address(BaseModel):
    street: str
    city: str
    manufacturer_id: int = Field()
    some: Some


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


def get_record_title(model: Item) -> Optional[str]:
    return f'{model.name} - {model.price}$'


class MyCustomManufacturerWidget(IntegerWidget):
    def __init__(self, available_manufacturers: list[int], **kwargs):
        super().__init__(**kwargs)
        self.available_manufacturers = available_manufacturers

    def render(self) -> ValidationElement:
        el = super().render()
        ui.label(
            text=f'Доступные ID производителей на текущий момент: {self.available_manufacturers}.'
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
        )

        form.custom_widget(
            field_name='items',
            widget=ListBaseModelWidget,
            title_getter=get_record_title,
        )

        items_list_widget = form.widgets['items']
        items_list_widget.form.custom_widget(
            field_name='manufacturer_id',
            widget=MyCustomManufacturerWidget,
            available_manufacturers=FAKE_DB['available_manufacturers'],
        )

        address_widget = form.widgets['address']
        address_widget.form.custom_widget(
            field_name='manufacturer_id',
            widget=MyCustomManufacturerWidget,
            available_manufacturers=FAKE_DB['available_manufacturers'],
        )

        some_widget = address_widget.form.widgets['some']
        some_widget.form.custom_widget(
            field_name='manufacturer_id',
            widget=MyCustomManufacturerWidget,
            available_manufacturers=FAKE_DB['available_manufacturers'],
        )

        form.render()
