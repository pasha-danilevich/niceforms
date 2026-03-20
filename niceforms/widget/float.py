from typing import Optional

from nicegui import ui

from niceforms.widget import BaseWidget, RenderedWidget


class RenderedFloatWidget(RenderedWidget):

    def collect(self) -> Optional[float]:
        if self.element.value is None:
            return None

        return self.element.value


class FloatWidget(BaseWidget):
    def render(self) -> RenderedWidget:
        el = (
            ui.number(
                value=self.default_value,
                placeholder=self.placeholder,
            )
            .props("outlined dense")
            .classes("w-full")
        )

        return RenderedFloatWidget(self, el)
