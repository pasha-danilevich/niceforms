from typing import Optional

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.button import Button
from nicegui.elements.mixins.name_element import NameElement

from niceforms import UIComponent
from niceforms.constants import DEFAULT_PADDING, PRIMARY_COLOR_GRADIENT


class Header(UIComponent):
    TIPS: str = "Поля со * (звездочкой) обязательные."

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
        self._description: Optional[Element] = None
        self._icon: Optional[NameElement] = None

    def toggle_expand_parent(self) -> None:
        if self._is_expanded:
            self.parent_card.style('height: 100px')
            self._is_expanded = False
            self._icon.props('name=unfold_more')  # иконка развернуть
            self._icon.tooltip('Развернуть')
            if self._description:
                self._description.set_visibility(False)
        else:
            self.parent_card.style('height: 100%')
            self._is_expanded = True
            self._icon.props('name=unfold_less')  # иконка свернуть
            self._icon.tooltip('Свернуть')
            if self._description:
                self._description.set_visibility(True)

    def render(self) -> None:
        with ui.element().classes(f"w-full {DEFAULT_PADDING} rounded-lg").style(
            f'background: {self.bg_color}'
        ):
            # Контейнер для заголовка и кнопки
            with ui.element().classes("flex justify-between items-start"):
                ui.label(self.title).classes("text-2xl font-bold text-white")

                # Иконка с подсказкой
                if not self.is_nested:
                    with ui.element().classes("cursor-help"):
                        ui.icon("help_outline", size="sm").classes(
                            "text-white/70 hover:text-white transition-colors"
                        )
                        ui.tooltip(self.TIPS)

                if self.is_nested:
                    self._icon = (
                        ui.icon('unfold_more', size="md")
                        .classes(
                            "cursor-pointer text-white/70 hover:text-white "
                            "transition-all duration-200"
                        )
                        .tooltip('Развернуть')
                    )
                    self._icon.on('click', self.toggle_expand_parent)

            if self.description:
                self._description = (
                    ui.label(self.description).classes("mt-2").style('color: #ffffff')
                )
                if self.is_nested:
                    self._description.set_visibility(False)
