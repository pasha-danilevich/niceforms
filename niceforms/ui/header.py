from typing import Optional

from nicegui import ui

from niceforms import UIComponent
from niceforms.constants import DEFAULT_PADDING, PRIMARY_COLOR_GRADIENT

class Header(UIComponent):
    def __init__(
        self,
        title: str,
        description: Optional[str],
        bg_color: Optional[str] = None,
    ) -> None:
        self.title = title
        self.description = description
        self.bg_color = bg_color if bg_color else PRIMARY_COLOR_GRADIENT

    def render(self) -> None:
        with ui.element().classes(
            f"w-full {DEFAULT_PADDING}  rounded-lg"
        ).style(f'background: {self.bg_color}'):
            ui.label(self.title).classes("text-2xl font-bold text-white")

            if self.description:
                ui.label(self.description).classes("text-blue-100 mt-2")
