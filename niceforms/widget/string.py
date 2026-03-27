from typing import Optional

from nicegui import ui
from nicegui.elements.mixins.validation_element import ValidationElement

from niceforms import BaseValidationWidget


class StringWidget(BaseValidationWidget):

    def collect(self) -> Optional[str]:
        if self.element.value == '':
            return None

        return self.element.value

    def render(self) -> ValidationElement:

        el = (
            ui.input(
                value=self.default_value,
                placeholder=self.placeholder,
                validation=self.default_validations,
            )
            .props("outlined dense")
            .classes("w-full")
        )

        return el
