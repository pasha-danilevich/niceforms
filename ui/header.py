from typing import Any, Optional

from nicegui import ui

from ui.components import UIComponent
from utils import PRIMARY_COLOR_GRADIENT, DEFAULT_PADDING


class Header(UIComponent):
    def __init__(self, title: str, description: Optional[str],) -> None:
        self.title = title
        self.description = description

    def render(self) -> None:
        with ui.column().classes(f"w-full {PRIMARY_COLOR_GRADIENT} {DEFAULT_PADDING}  rounded-lg"):
            ui.label(self.title).classes("text-2xl font-bold text-white")

            if self.description:
                ui.label(self.description).classes("text-blue-100 mt-2")