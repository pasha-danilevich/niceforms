from _layout import base
from nicegui import APIRouter, ui

from niceforms import BaseModelForm

router = APIRouter()


from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int


class Room(BaseModel):
    number: int
    floor: int
    peoples: list[Person]


# вот как, скорее всего, получится отобразить widget list[BaseModel]

# 1. Коля               [показать] [редактировать] [удалить]
# 2. Вася               [показать] [редактировать] [удалить]
# 3. Миша               [показать] [редактировать] [удалить]

# то есть тут можно попытаться из модели Person получить первый попавшийся строчный атрибут и использовать его в виде title

# в случае, когда у модели не будет строчных атрибутов, просто отображаем как "запись":

# 1. Запись №1           [показать] [редактировать] [удалить]
# 2. Запись №2           [показать] [редактировать] [удалить]
# 3. Запись №3           [показать] [редактировать] [удалить]


@router.page('/list_model')
@base
async def list_model() -> None:
    with ui.column().classes('w-full max-w-2xl mx-auto'):
        ui.link(text='Назад', target='/')

        async def submit_handler(model: BaseModel) -> None:
            print(f"{model}")

        form = BaseModelForm(Room, on_submit=submit_handler, view_annotation_type=False)
        form.render()
