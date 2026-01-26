from nicegui import ui

from ui.components import UIComponent
from utils import DEFAULT_PADDING


class Body(UIComponent):
    def __init__(self, widgets: list[UIComponent]) -> None:
        self.widgets = widgets

    def render(self) -> None:
        with ui.column().classes(f"w-full {DEFAULT_PADDING} space-y-6"):
            for w in self.widgets:
                w.render()
