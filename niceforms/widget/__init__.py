"""Виджеты для полей формы."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

from nicegui import ui
from nicegui.elements.button import Button
from nicegui.elements.mixins.value_element import ValueElement
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from niceforms import UIComponent

logger = logging.getLogger(__name__)


class BaseWidget(UIComponent, ABC):
    def __init__(
        self,
        field_info: FieldInfo,
        field_name: str,
        is_nullable: bool,
        view_annotation_type: bool
    ):
        self.field = field_info
        self.field_name = field_name
        self.is_nullable = is_nullable
        self.view_annotation_type = view_annotation_type

        self.set_none_button: Optional[Button] = None

    @property
    def placeholder(self) -> str:
        return (
            f"Введите {self.field.title.lower()}"
            if self.field.title
            else "Введите значение"
        )

    @property
    def default_value(self) -> Optional[Any]:
        return (
            self.field.default if self.field.default is not PydanticUndefined else None
        )

    def render_label(self) -> None:
        text = self.field.title if self.field.title else self.field_name.title()
        logger.debug(f"render label: {text}")

        with ui.row().classes('mb-1 items-baseline justify-between w-full gap-1'):
            with ui.row().classes('items-baseline gap-1'):
                ui.label(text=text).classes('font-bold text-lg')
                if self.field.is_required():
                    ui.label(text='*').classes('text-gray-400 text-md font-normal')
                if self.view_annotation_type:
                    ui.label(text=f' [{self.field.annotation}]').classes(
                        'text-gray-400 text-md font-normal'
                    )

            if self.is_nullable:

                self.set_none_button = ui.button('Set None', color='secondary').classes(
                    'text-xs opacity-70 hover:opacity-100 transition-opacity py-0.7 px-2 min-h-0 h-auto'
                )

        if self.field.description:
            ui.label(text=self.field.description).classes("mb-1 text-gray-500")

    @abstractmethod
    def render(
        self,
    ) -> (
        "RenderedWidget"
    ):  # TODO: возможно достаточно будет в RenderedWidget передавать в место BaseWidget "field_name"
        raise NotImplementedError


class RenderedWidget(ABC):
    def __init__(self, widget: BaseWidget, element: ValueElement) -> None:
        self.widget = widget
        self.element = element

        self._none_is_set = False

        if self.widget.set_none_button:

            def on_click_set_none() -> None:
                if self._none_is_set:
                    self.widget.set_none_button.text = 'Set None'
                    self._none_is_set = False
                else:
                    self.element.value = None
                    self.widget.set_none_button.text = 'None is set'
                    self._none_is_set = True

            self.widget.set_none_button.on_click(on_click_set_none)

    def clear(self) -> None:
        self.element.set_value(None)

    @abstractmethod
    def collect(self) -> Optional[Any]:
        raise NotImplementedError
