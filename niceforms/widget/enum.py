from typing import Any, Optional

from nicegui import ui

from niceforms.widget import BaseWidget, RenderedWidget


class RenderedEnumWidget(RenderedWidget):

    def collect(self) -> Optional[Any]:
        return self.element.value


class EnumWidget(BaseWidget):
    """Виджет для полей типа Enum с выплывающим списком"""

    def render(self) -> RenderedEnumWidget:
        print(f'{self.field_name}: {self.normalized_type.origin_type}')
        options = list(self.normalized_type.origin_type)

        s = (
            ui.select(
                label='Выберите значение',
                value=self.default_value,
                options=options,
            )
            .props("outlined dense")
            .classes("w-full")
        )

        return RenderedEnumWidget(self, s)
