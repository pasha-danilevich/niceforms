from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement

from niceforms.widget import BaseWidget


class StringWidget(BaseWidget):

    def render(self) -> ValueElement:
        el = ui.input(value=self.default_value, placeholder=self.placeholder).props("outlined dense").classes("w-full")
        return el
