from typing import Any, Optional

from nicegui import ui

from niceforms.widget import BaseWidget, RenderedWidget


class RenderedBoolWidget(RenderedWidget):

    def collect(self) -> Optional[Any]:
        return self.element.value


class BoolWidget(BaseWidget):

    def render(self) -> RenderedBoolWidget:

        checkbox = (
            ui.checkbox(
                text='Выставьте checkbox',
                value=self.default_value,
            )
            .props("outlined dense")
            .classes("w-full")
        )

        return RenderedBoolWidget(self, checkbox)
