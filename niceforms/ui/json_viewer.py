from nicegui import ui
from pydantic import BaseModel

from niceforms import UIComponent


class JsonDialog(UIComponent):
    def __init__(self, model: BaseModel):
        self.model = model

    def render(self) -> None:

        json_data = {'content': {'json': self.model.model_dump()}}

        with ui.dialog() as dialog, ui.card():
            ui.label('Результирующий JSON объект').classes('text-h5 font-bold')
            ui.label('(только чтение)')

            # ui.json автоматически красиво форматирует JSON
            ui.json_editor(json_data).classes('w-full')

            with ui.row().classes('justify-end w-full mt-4'):
                ui.button('Close', on_click=dialog.close).props('flat')

        dialog.open()
