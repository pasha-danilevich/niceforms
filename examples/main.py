import logging

logging.basicConfig(level=logging.DEBUG)

"""Базовый пример использования."""
import basic
import complex_type
import nested
from _layout import base
from nicegui import app, ui


@ui.page('/')
@base
async def index() -> None:
    ui.link(text='Обычное использование', target='/basic')
    ui.link(text='Вложенная модель', target='/nested')
    ui.link(text='Сложные типы', target='/complex_type')


app.include_router(basic.router)
app.include_router(nested.router)
app.include_router(complex_type.router)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(show=False, reload=False)
