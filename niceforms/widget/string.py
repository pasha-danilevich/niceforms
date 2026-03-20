from typing import Any, Optional

from nicegui import ui
from pydantic_core import PydanticUndefinedType

from niceforms.widget import BaseWidget, RenderedWidget


class RenderedStringWidget(RenderedWidget):
    def clear(self) -> None:
        if self.widget.field.default is not None and not PydanticUndefinedType:
            self.element.set_value(self.widget.field.default)


    def collect(self) -> Optional[str]:
        if self.element.value == '':
            return None

        return self.element.value


class StringWidget(BaseWidget):

    def render(self) -> RenderedWidget:
        el = ui.input(value=self.default_value, placeholder=self.placeholder).props("outlined dense").classes("w-full")
        return RenderedStringWidget(self, el)
