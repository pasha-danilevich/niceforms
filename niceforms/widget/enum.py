from typing import Any, Optional

from nicegui import ui
from nicegui.elements.mixins.validation_element import ValidationElement

from widget import BaseValidationWidget


class EnumWidget(BaseValidationWidget):
    """Виджет для полей типа Enum с выплывающим списком"""

    def collect(self) -> Optional[Any]:
        return self.element.value

    def render(self) -> ValidationElement:
        options = list(self.normalized_type.origin_type)

        select = (
            ui.select(
                label='Выберите значение',
                value=self.default_value,
                options=options,
                validation=self.default_validations,
            )
            .props("outlined dense")
            .classes("w-full")
        )

        return select
