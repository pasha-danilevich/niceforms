"""Пример работы с валидацией и ошибками Pydantic.

Что происходит:

Заданы ограничения (min_length, pattern, ge, и т.д.)
Добавлен кастомный перевод ошибок через tr.add_custom_translations

Что полезного показывает:

Как отображаются ошибки пользователю
Как кастомизировать тексты ошибок"""

from nicegui import APIRouter, ui
from pydantic import BaseModel, Field

from ._layout import base, TheNavigation
from niceforms import BaseModelForm
from niceforms.i18n import tr

router = APIRouter()


tr.add_custom_translations(
    {
        'string_too_short': (
            'Минимальная длина {min_length}. Это мой кастомный перевод!!!'
        )
    },
)


class User(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Z]+$",
        title="Имя",
    )

    age: int = Field(ge=14, lt=150, description="Возраст пользователя")

    salary: float = Field(ge=0, multiple_of=0.01)

    tags: list[str] = Field(min_length=1, max_length=3)


@router.page('/pydantic_error_catching')
@base
async def pydantic_error_catching() -> None:
    with ui.column().classes('w-full max-w-2xl mx-auto'):
        TheNavigation(
            description='Когда важен UX и понятные ошибки для пользователя'
        ).render()

        async def submit_handler(model: User) -> None:
            print(f"Пользователь создан: {model}")

        form = BaseModelForm[User](User, on_submit=submit_handler, view_annotation_type=False)
        form.render()
