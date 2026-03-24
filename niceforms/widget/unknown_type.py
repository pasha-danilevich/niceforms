from typing import Any, Optional

from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement

from niceforms.widget import BaseWidget


class UnknownTypeWidget(BaseWidget):
    """Для неизвестных типов предлагается вводить JSON строку"""

    def collect(self) -> Optional[Any]:
        return self.element.value

    def render(self) -> ValueElement:
        el = (
            ui.input(
                value=self.default_value,
                placeholder=self.placeholder,
            )
            .classes('w-full font-mono')
            .props("outlined dense")
        )

        ui.label(
            text=f'Для типа "{self.field.annotation}" не существует виджета. Предоставлен обычный ввод строки.'
        ).classes('text-xs mt-1').style('color: #ff3a3a')

        return el
