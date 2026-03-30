from typing import Any, Optional, Hashable

from nicegui import ui
from nicegui.elements.mixins.validation_element import ValidationElement

from niceforms import BaseValidationWidget


class SelectWidget(BaseValidationWidget):

    def __init__(
        self,
        options: dict[Hashable, str],
        label: str = 'Выберите значение',
        multiple: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.options = options
        self.label = label
        self.multiple = multiple

    def collect(self) -> Optional[Any]:
        return self.element.value

    def render(self) -> ValidationElement:
        value = self.options.get(self.default_value)

        select = (
            ui.select(
                label=self.label,
                value=value,
                options=self.options,
                validation=self.default_validations,
                multiple=self.multiple,
            )
            .props("outlined dense")
            .classes("w-full")
        )

        return select
