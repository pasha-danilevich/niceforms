from typing import Any, Optional, Union

from nicegui import ui

from niceforms.widget import BaseWidget, RenderedWidget


class RenderedIterableWidget(RenderedWidget):

    def collect(self) -> Optional[Union[list, tuple]]:
        return self.element.value


class IterableWidget(BaseWidget):

    def render(self) -> RenderedWidget:
        el = ui.input()
        el.delete()
        with ui.list().props('bordered separator') as l:
            with ui.item():
                with ui.item_section().props('avatar'):
                    ui.label('#1')
                with ui.item_section():
                    ui.item_label('Nice Person')
                with ui.item(on_click=lambda e: ui.notify(f'delete')):
                    with ui.item_section():
                        ui.icon('backspace')
            with ui.item():
                with ui.item_section():
                    ui.input(placeholder='Введите значение')
                with ui.item_section().props('avatar'):
                    with ui.item(on_click=lambda e: ui.notify(f'add')):
                        with ui.item_section():
                            ui.icon('add')

        print(l)

        return RenderedIterableWidget(self, el)
