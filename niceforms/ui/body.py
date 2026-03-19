from nicegui import ui
from nicegui.elements.mixins.value_element import ValueElement

from niceforms import UIComponent
from widget import BaseWidget, RenderedWidget


class Body:
    def __init__(self, widgets: list[BaseWidget]) -> None:
        self.widgets = widgets

    def render(self) -> list[RenderedWidget]:
        elements = []

        with ui.column().classes(f"w-full p-4 space-y-3"):
            for w in self.widgets:
                with ui.element().classes(f"w-full"):
                    w.render_label()
                    el = w.render()
                    elements.append(el)

        return elements