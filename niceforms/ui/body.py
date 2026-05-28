from typing import cast, Optional

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.mixins.validation_element import ValidationElement
from niceforms.widget import BaseWidget, BaseValidationWidget


class Body:
    def __init__(self, widgets: list[BaseWidget]) -> None:
        self.widgets = widgets
        self._root: Optional[Element] = None

    @property
    def root(self) -> Element:
        if self._root is None:
            raise ValueError("Not rendered")
        return self._root


    def render(self) -> Element:
        widgets = []

        with ui.column().classes(f"w-full p-1 sm:p-4 gap-[0px]") as self._root:
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

        return self.root
