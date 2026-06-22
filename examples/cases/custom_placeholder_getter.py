from typing import Optional

from nicegui import APIRouter, ui
from pydantic import BaseModel, Field

from niceforms import BaseModelForm, BaseWidget
from niceforms.widget.integer import IntegerWidget
from niceforms.widget_factory import WidgetFactory
from ._layout import base, TheNavigation
router = APIRouter()


class User(BaseModel):
    """Просто пользователь"""

    name: str = Field(default='Петя', title="Имя")
    surname: str = Field(..., description="Фамилия пользователя")
    height: Optional[int]


def my_custom_placeholder_getter(widget: BaseWidget) -> Optional[str]:
    return f'my custom placeholder: {widget.field_name}'

def exclusive_widget_custom_placeholder(widget: BaseWidget) -> Optional[str]:
    return f"field name is: {widget.field_name}"

@router.page('/placeholder')
@base
async def basic() -> None:
    WidgetFactory.print_widget_registry()

    with ui.column().classes('w-full max-w-2xl mx-auto'):
        TheNavigation(description='Кастомизация placeholder').render()

        async def submit_handler(model: User) -> None:
            print(f"Пользователь создан: {model}")

        form = BaseModelForm(
            User,
            on_submit=submit_handler,
            view_annotation_type=False,
            placeholder_getter=my_custom_placeholder_getter,
        )
        form.custom_widget("height", IntegerWidget, placeholder_getter=exclusive_widget_custom_placeholder)

        form.render()