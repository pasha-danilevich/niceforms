"""
Что происходит:

Пользователь заполняет форму
Каждые 5 секунд данные сохраняются в app.storage.user
Если страницу перезагрузить — форма восстановится из сохранённых данных

Что полезного показывает:

Как реализовать черновики формы
Как использовать form.collect_data() без валидации
Как заполнять форму через form.fill()
"""

from enum import Enum
from typing import Optional

from _layout import base, TheNavigation
from nicegui import APIRouter, ui, app
from pydantic import BaseModel, Field


from niceforms import BaseModelForm

router = APIRouter()


class Style(str, Enum):
    Red = "red"
    Green = "green"
    Yellow = "yellow"


class User(BaseModel):
    """Просто пользователь"""

    name: str = Field(title="Имя")
    surname: str = Field(..., description="Фамилия пользователя")
    height: Optional[int]
    style: Style = Style.Yellow


@router.page('/auto_save')
@base
async def basic() -> None:
    with ui.column().classes('w-full max-w-2xl mx-auto'):
        TheNavigation(
            description='Когда не хочется терять введённые данные (длинные формы, анкеты и т.д.)'
        ).render()

        async def submit_handler(user: BaseModel) -> None:
            print(f"Пользователь создан: {user}")

        form = BaseModelForm(User, on_submit=submit_handler, view_annotation_type=False)
        form.render()

    storage_key = f'cache_form_{form.model.__name__}_3'

    save_form_data = app.storage.user.get(storage_key)
    print(f'{save_form_data=}')

    def clean_dict_none(data: dict) -> dict:
        """Возвращает новый словарь без ключей, у которых значение None"""
        return {key: value for key, value in data.items() if value is not None}

    if save_form_data:
        form.fill(data=clean_dict_none(save_form_data))

    def cache_from_data() -> None:
        print('cache_from_data')
        app.storage.user[storage_key] = form.collect_data(validate=False)

    ui.timer(interval=5, callback=cache_from_data, immediate=False)
