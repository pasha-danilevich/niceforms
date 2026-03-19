from typing import Optional

from nicegui import ui
from nicegui.elements.button import Button
from nicegui.elements.mixins.value_element import ValueElement
from pydantic import BaseModel

from niceforms import UIComponent, PRIMARY_COLOR_GRADIENT
from widget import RenderedWidget


class Footer(UIComponent):
    def __init__(self, elements: list[RenderedWidget], is_nested: bool) -> None:
        self.elements = elements
        self.is_nested = is_nested

        self._write_to_form_button: Optional[Button] = None
        self._submit_button: Optional[Button] = None

    def validate_form(self) -> Optional[BaseModel]:
        pass

    def clear_form(self) -> None:
        print('Cleared form')
        for element in self.elements:
            element.clear()

    def render_json_viewer_dialog(self) -> None:
        pass

    def _write_nested_form_to_main_form(self) -> None:
        pass

    async def submit(self) -> None:
        for element in self.elements:
            x = element.collect()
            print(x)

    def render(self) -> None:
        with ui.row().classes("w-full justify-end gap-3"):
            ui.button("Очистить", on_click=self.clear_form).props(
                "outlined flat"
            ).classes("px-6 py-2")

            ui.button("Показать json", on_click=self.render_json_viewer_dialog).props(
                "outlined flat"
            ).classes("px-6 py-2")



            if self.is_nested:
                self._write_to_form_button = (
                    ui.button("Сохранить в форму", on_click=self._write_nested_form_to_main_form)
                    .props("unelevated")
                    .classes(f"{PRIMARY_COLOR_GRADIENT} text-white px-8 py-2")
                )
            else:
                self._submit_button = (
                    ui.button("Отправить", on_click=self.submit, icon="send")
                    .props("unelevated")
                    .classes(f"{PRIMARY_COLOR_GRADIENT} text-white px-8 py-2")
                )
