from typing import Any, Optional

from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement

from niceforms.widget import BaseWidget


class EnumWidget(BaseWidget):
    """Виджет для полей типа Enum с выплывающим списком"""

    def collect(self) -> Optional[Any]:
        return self.element.value

    def render(self) -> ValueElement:
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
