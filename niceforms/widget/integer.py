from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement

from niceforms.widget import BaseWidget


class IntegerWidget(BaseWidget):
    def render(self) -> ValueElement:
        el = ui.number(
            value=self.default_value,  # должно быть число, не текст
            placeholder=self.placeholder,
        ).props("outlined dense").classes("w-full")
        return el
