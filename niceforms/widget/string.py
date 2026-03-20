from typing import Any, Optional

from nicegui import ui
from pydantic_core import PydanticUndefinedType

from niceforms.widget import BaseWidget, RenderedWidget


class RenderedStringWidget(RenderedWidget):

    def collect(self) -> Optional[str]:
        if self.element.value == '':
            return None

        return self.element.value


class StringWidget(BaseWidget):

    def render(self) -> RenderedWidget:
        el = ui.input(value=self.default_value, placeholder=self.placeholder).props("outlined dense").classes("w-full")
        return RenderedStringWidget(self, el)
