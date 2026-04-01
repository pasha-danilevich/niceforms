import logging

logging.basicConfig(level=logging.DEBUG)

"""Базовый пример использования."""
import basic
import complex_type
import list_model
import many_forms
import nested
import fill_form
import auto_save
import custom_field_widget
import select_widget
import pydantic_error_catching
from _layout import base
from nicegui import app, ui


@ui.page('/')
@base
async def index() -> None:
    ui.link(text='Обычное использование', target='/basic')
    ui.link(text='Вложенная модель', target='/nested')
    ui.link(text='Сложные типы', target='/complex_type')
    ui.link(text='Много форм', target='/many_forms')
    ui.link(text='Списки', target='/list_model')
    ui.link(text='Заполненная форма', target='/fill_from')
    ui.link(text='Сохранение введенной формы', target='/auto_save')
    ui.link(text='Кастомизация виджета по полю', target='/custom_field_widget')
    ui.link(text='Select widget', target='/select')
    ui.link(text='Отлавливание Pydantic ошибок', target='/pydantic_error_catching')


app.include_router(basic.router)
app.include_router(nested.router)
app.include_router(complex_type.router)
app.include_router(many_forms.router)
app.include_router(list_model.router)
app.include_router(fill_form.router)
app.include_router(auto_save.router)
app.include_router(custom_field_widget.router)
app.include_router(select_widget.router)
app.include_router(pydantic_error_catching.router)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(show=False, reload=False, storage_secret='storage_secret')
