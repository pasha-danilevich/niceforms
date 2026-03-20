from typing import Optional

from nicegui import ui
from pydantic_core import PydanticUndefinedType

from niceforms.widget import BaseWidget, RenderedWidget


class RenderedIntegerWidget(RenderedWidget):
    def clear(self) -> None:
        if self.widget.field.default is not None and not PydanticUndefinedType:
            self.element.set_value(self.widget.field.default)

        self.element.set_value(None)

    def collect(self) -> Optional[int]:
        if self.element.value is None:
            return None

        return int(self.element.value)


class IntegerWidget(BaseWidget):
    def render(self) -> RenderedWidget:
        el = ui.number(
            value=self.default_value,
            placeholder=self.placeholder,
        ).props("outlined dense").classes("w-full")

        return RenderedIntegerWidget(self, el)
