from typing import cast

from nicegui import ui
from nicegui.elements.mixins.validation_element import ValidationElement
from widget import BaseWidget, BaseValidationWidget


class Body:
    def __init__(self, widgets: list[BaseWidget]) -> None:
        self.widgets = widgets

    def render(self) -> list[BaseWidget]:
        widgets = []

        with ui.column().classes(f"w-full p-1 sm:p-4 gap-[0px]"):
            for w in self.widgets:
                with ui.element().classes(f"w-full"):
                    w.render_label()
                    el = w.render()
                    w.set_element(el)

                    if not isinstance(w, BaseValidationWidget):
                        w.render_error()

                    if isinstance(w.element, ValidationElement):
                        el = cast(ValidationElement, w.element)
                        el.on('blur', el.validate)

                    widgets.append(w)

        return widgets
