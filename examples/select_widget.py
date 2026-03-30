"""Пример, когда в PydanticModel нужно записать число, например ID записи в БД,
а пользователю отобразить человеку понятный текст"""

from enum import Enum
from typing import Optional

from nicegui import APIRouter, ui
from pydantic import BaseModel, Field

from _layout import base
from niceforms import BaseModelForm
from niceforms.widget.select import SelectWidget

router = APIRouter()

FAKE_DATA = {
    'manufacturer': {
        1: 'The South Manufacturer',
        2: 'The West Builders etc',
        3: 'Corporation Manufacturer',
    },
    'equipment': {
        1: 'Winter tires',
        2: 'Air conditioner',
        3: 'DVD player',
        4: 'Signaling',
    },
}


class ItemColor(str, Enum):
    black = 'black'
    red = 'red'
    green = 'green'


class Item(BaseModel):
    name: str
    price: float = Field(ge=0, description='Price in USD')
    color: Optional[ItemColor]

    manufacturer_id: int
    equipments_id: list[int]


@router.page('/select')
@base
async def select() -> None:
    with ui.column().classes('w-full max-w-2xl mx-auto'):
        ui.link(text='Назад', target='/')

        async def submit_handler(model: BaseModel) -> None:
            print(model)

        form = BaseModelForm[Item](
            Item,
            on_submit=submit_handler,
            view_annotation_type=False,
        )

        form.custom_widget(
            field_name='manufacturer_id',
            widget=SelectWidget,
            options=FAKE_DATA['manufacturer'],
        )
        form.custom_widget(
            field_name='equipments_id',
            widget=SelectWidget,
            options=FAKE_DATA['equipment'],
            multiple=True,
        )

        form.render()
