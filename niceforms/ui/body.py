from typing import cast, Optional, Callable

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.mixins.validation_element import ValidationElement
from niceforms.widget import BaseWidget, BaseValidationWidget


class Body:
    def __init__(self, widgets: list[BaseWidget], render_widget: Callable[[BaseWidget], Element] | None) -> None:
        self.widgets = widgets
        self.render_widget = render_widget
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
                self.render_widget(w)
                widgets.append(w)

        return self.root
