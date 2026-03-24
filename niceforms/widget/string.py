from typing import Optional

from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement

from niceforms.widget import BaseWidget


class StringWidget(BaseWidget):

    def collect(self) -> Optional[str]:
        if self.element.value == '':
            return None

        return self.element.value

    def render(self) -> ValueElement:
        el = (
            ui.input(value=self.default_value, placeholder=self.placeholder)
            .props("outlined dense")
            .classes("w-full")
        )
        return el
