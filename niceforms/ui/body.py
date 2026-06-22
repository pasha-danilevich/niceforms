from typing import cast, Optional, Callable

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.mixins.validation_element import ValidationElement
from niceforms.widget import BaseWidget, BaseValidationWidget


class Body:
    def __init__(self, widgets: list[BaseWidget], render_widget: Callable[[BaseWidget], Element] | None, body_element_classes: str) -> None:
        self.widgets = widgets
        self.render_widget = render_widget
        self._root: Optional[Element] = None
        self._body_element_classes = body_element_classes

    @property
    def root(self) -> Element:
        if self._root is None:
            raise ValueError("Not rendered")
        return self._root


    def render(self) -> Element:
        widgets = []

        with ui.column().classes(self._body_element_classes) as self._root:
            for w in self.widgets:
                self.render_widget(w)
                widgets.append(w)

        return self.root
