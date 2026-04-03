import logging

logging.basicConfig(level=logging.DEBUG)

"""Базовый пример использования."""
from cases import basic
from cases import complex_type
from cases import list_model
from cases import many_forms
from cases import nested
from cases import fill_form
from cases import auto_save
from cases import custom_field_widget
from cases import custom_type_widget
from cases import select_widget
from cases import pydantic_error_catching
from cases import disable_widget


from nicegui import app, ui


@ui.page('/')
async def index() -> None:
    ui.link(text='Обычное использование', target='/basic')
    ui.link(text='Вложенная модель', target='/nested')
    ui.link(text='Сложные типы', target='/complex_type')
    ui.link(text='Много форм', target='/many_forms')
    ui.link(text='Списки', target='/list_model')
    ui.link(text='Заполненная форма', target='/fill_from')
    ui.link(text='Сохранение введенной формы', target='/auto_save')
    ui.link(text='Кастомизация виджета по полю', target='/custom_field_widget')
    ui.link(text='Кастомизация виджета по типу', target='/custom_type_widget')
    ui.link(text='Select widget', target='/select')
    ui.link(text='Отлавливание Pydantic ошибок', target='/pydantic_error_catching')
    ui.link(text='Отключение виджета', target='/disable_widget')


app.include_router(basic.router)
app.include_router(nested.router)
app.include_router(complex_type.router)
app.include_router(many_forms.router)
app.include_router(list_model.router)
app.include_router(fill_form.router)
app.include_router(auto_save.router)
app.include_router(custom_field_widget.router)
app.include_router(custom_type_widget.router)
app.include_router(select_widget.router)
app.include_router(pydantic_error_catching.router)
app.include_router(disable_widget.router)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(show=False, reload=False, storage_secret='storage_secret')
