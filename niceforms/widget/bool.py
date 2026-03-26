from typing import Any, Optional

from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement

from widget import BaseValueWidget


class BoolWidget(BaseValueWidget):
    def validate(self) -> Optional[str]:
        return None

    def collect(self) -> Optional[Any]:
        return self.element.value

    def render(self) -> ValueElement:
        el = (
            ui.checkbox(
                text='Выставьте checkbox',
                value=self.default_value,
            )
            .props("outlined dense")
            .classes("w-full")
        )

        return el
