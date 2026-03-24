import logging
from typing import Optional

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.button import Button
from nicegui.elements.mixins.name_element import NameElement

from niceforms import UIComponent
from niceforms.constants import DEFAULT_PADDING, PRIMARY_COLOR_GRADIENT

logger = logging.getLogger(__name__)


class Header(UIComponent):
    TIPS: str = "Поля со * (звездочкой) обязательные."

    def __init__(
        self,
        title: str,
        description: Optional[str],
        parent_card: Element,
        is_nested: bool,
        is_nullable: bool = False,
        bg_color: Optional[str] = None,
    ) -> None:
        self.title = title
        self.description = description
        self.parent_card = parent_card
        self.is_nested = is_nested
        self.is_nullable = is_nullable
        self.bg_color = bg_color if bg_color else PRIMARY_COLOR_GRADIENT

        self._is_expanded = False
        self._button: Optional[Button] = None
        self._description: Optional[Element] = None
        self._icon: Optional[NameElement] = None
        self._delete_icon: Optional[NameElement] = None
        self._main_container: Optional[Element] = None

        self._is_none: bool = False

    @property
    def is_none(self) -> bool:
        return self._is_none

    def toggle_is_none(self) -> bool:
        self._is_none = not self._is_none
        logger.debug(f"do toggle_is_none: {self._is_none=}")

        # Обновляем стиль при переключении
        if self._main_container:
            if self._is_none:
                self._main_container.style('background: #6c757d')  # Серый цвет
                if self._delete_icon:
                    self._delete_icon.props('name=restore_from_trash')
                    self._delete_icon.tooltip('Восстановить')
            else:
                self._main_container.style(f'background: {self.bg_color}')
                if self._delete_icon:
                    self._delete_icon.props('name=delete_outline')
                    self._delete_icon.tooltip('Удалить')

        return self._is_none

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
        self._main_container = (
            ui.element()
            .classes(f"w-full {DEFAULT_PADDING} rounded-lg")
            .style(f'background: {self.bg_color}')
        )

        with self._main_container:
            # Контейнер для заголовка и кнопок
            with ui.element().classes("flex justify-between items-start"):
                ui.label(self.title).classes("text-2xl font-bold text-white")

                # Контейнер для иконок справа
                with ui.element().classes("flex gap-2 items-center"):
                    # Иконка подсказки (только для невложенных)
                    if not self.is_nested:
                        with ui.element().classes("cursor-help"):
                            ui.icon("help_outline", size="sm").classes(
                                "text-white/70 hover:text-white transition-colors"
                            )
                            ui.tooltip(self.TIPS)

                    # Иконка удаления/восстановления
                    if self.is_nested and self.is_nullable:
                        self._delete_icon = (
                            ui.icon('delete_outline', size="md")
                            .classes(
                                "cursor-pointer text-white/70 hover:text-white "
                                "transition-all duration-200"
                            )
                            .tooltip('Удалить')
                        )
                        self._delete_icon.on('click', self.toggle_is_none)

                    # Иконка развернуть/свернуть
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
