from typing import Optional

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.button import Button

from niceforms import UIComponent
from niceforms.constants import DEFAULT_PADDING, PRIMARY_COLOR_GRADIENT


class Header(UIComponent):
    def __init__(
        self,
        title: str,
        description: Optional[str],
        parent_card: Element,
        is_nested: bool,
        bg_color: Optional[str] = None,
    ) -> None:
        self.title = title
        self.description = description
        self.parent_card = parent_card
        self.is_nested = is_nested
        self.bg_color = bg_color if bg_color else PRIMARY_COLOR_GRADIENT

        self._is_expanded = False
        self._button: Optional[Button] = None

    def toggle_expand_parent(self) -> None:
        if self._is_expanded:
            self.parent_card.style('height: 100px')
            self._is_expanded = False
            self._button.text = 'Развернуть'
        else:
            self.parent_card.style('height: 100%')
            self._is_expanded = True
            self._button.text = 'Свернуть'

    def render(self) -> None:
        with ui.element().classes(f"w-full {DEFAULT_PADDING} rounded-lg").style(
            f'background: {self.bg_color}'
        ):
            # Контейнер для заголовка и кнопки
            with ui.element().classes("flex justify-between items-start"):
                ui.label(self.title).classes("text-2xl font-bold text-white")

                if self.is_nested:
                    self._button = ui.button('Развернуть', on_click=self.toggle_expand_parent).classes(
                        "px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg text-white "
                        "transition-all duration-200 text-sm font-medium"
                    ).props("outlined flat")

            if self.description:
                ui.label(self.description).classes("text-blue-100 mt-2")
