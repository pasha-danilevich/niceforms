from typing import Optional

from nicegui import ui
from nicegui.elements.mixins.validation_element import ValidationElement

from widget import BaseValidationWidget


class FloatWidget(BaseValidationWidget):
    def collect(self) -> Optional[float]:
        if self.element.value is None:
            return None

        return self.element.value

    def render(self) -> ValidationElement:
        el = (
            ui.number(
                value=self.default_value,
                placeholder=self.placeholder,
                validation=self.default_validations,
            )
            .props("outlined dense")
            .classes("w-full")
        )

        return el
