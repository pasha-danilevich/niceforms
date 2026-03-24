from typing import Optional

from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement

from niceforms.widget import BaseWidget


class IntegerWidget(BaseWidget):
    def collect(self) -> Optional[int]:
        if self.element.value is None:
            return None

        return int(self.element.value)

    def render(self) -> ValueElement:
        el = (
            ui.number(
                value=self.default_value,
                placeholder=self.placeholder,
            )
            .props("outlined dense")
            .classes("w-full")
        )

        return el
