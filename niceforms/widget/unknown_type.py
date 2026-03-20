from typing import Optional

from nicegui import ui
from pydantic_core import PydanticUndefinedType

from niceforms.widget import BaseWidget, RenderedWidget


class RenderedUnknownTypeWidget(RenderedWidget):
    def clear(self) -> None:
        if self.widget.field.default is not None and not PydanticUndefinedType:
            self.element.set_value(self.widget.field.default)

        if self.widget.is_nullable:
            self.element.set_value(None)

    def collect(self) -> Optional[int]:
        return self.element.value


class UnknownTypeWidget(BaseWidget):
    """Для неизвестных типов предлагается вводить JSON строку"""

    def render(self) -> RenderedWidget:
        el = (
            ui.input(
                value=self.default_value,
                placeholder=self.placeholder,
                # on_change=self._validate_json,
            )
            .classes('w-full font-mono')
            .props("outlined dense")
        )

        # Добавляем подсказку о формате JSON
        ui.label(
            text=f'Для типа "{self.field.annotation}" не существует виджета. Предоставлен обычный ввод строки.'
        ).classes('text-xs mt-1').style('color: #ff3a3a')

        return RenderedUnknownTypeWidget(self, el)
