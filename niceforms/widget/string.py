from typing import Any

from nicegui import ui

from niceforms.widget import BaseWidget, RenderedWidget


class RenderedStringWidget(RenderedWidget):
    def clear(self) -> None:
        self.element.set_value('')

    def collect(self) -> str:
        return self.element.value


class StringWidget(BaseWidget):

    def render(self) -> RenderedWidget:
        el = ui.input(value=self.default_value, placeholder=self.placeholder).props("outlined dense").classes("w-full")
        return RenderedStringWidget(self, el)
